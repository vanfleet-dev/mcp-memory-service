"""
Tests for SQLite WAL mode and concurrent access functionality.
"""

import pytest
import pytest_asyncio
import sqlite3
import os
import tempfile
import asyncio
import time
from unittest.mock import patch, MagicMock
from concurrent.futures import ThreadPoolExecutor

from mcp_memory_service.storage.sqlite_vec import SqliteVecMemoryStorage
from mcp_memory_service.models.memory import Memory


class TestWALMode:
    """Test suite for WAL mode and concurrent access features."""
    
    @pytest_asyncio.fixture
    async def storage(self):
        """Create a temporary SQLite storage instance."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            db_path = tmp.name
        
        storage = SqliteVecMemoryStorage(db_path)
        await storage.initialize()
        yield storage
        
        # Cleanup
        storage.close()
        try:
            os.unlink(db_path)
            os.unlink(db_path + "-wal")  # Remove WAL file
            os.unlink(db_path + "-shm")  # Remove shared memory file
        except:
            pass
    
    @pytest.mark.asyncio
    async def test_wal_mode_enabled(self, storage):
        """Test that WAL mode is properly enabled."""
        # Check journal mode
        cursor = storage.conn.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]
        assert journal_mode.upper() == "WAL"
        
        # Check other pragmas
        cursor = storage.conn.execute("PRAGMA busy_timeout")
        busy_timeout = cursor.fetchone()[0]
        assert busy_timeout == 5000
        
        cursor = storage.conn.execute("PRAGMA synchronous")
        synchronous = cursor.fetchone()[0]
        assert synchronous in [1, "NORMAL"]  # SQLite may return int or string
    
    @pytest.mark.asyncio
    async def test_custom_pragma_env_variable(self):
        """Test that custom pragmas from environment variables are applied."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            db_path = tmp.name
        
        # Set custom pragmas via environment variable
        with patch.dict(os.environ, {
            "MCP_MEMORY_SQLITE_PRAGMAS": "busy_timeout=10000,cache_size=20000"
        }):
            storage = SqliteVecMemoryStorage(db_path)
            await storage.initialize()
            
            # Check custom pragmas were applied
            cursor = storage.conn.execute("PRAGMA busy_timeout")
            assert cursor.fetchone()[0] == 10000
            
            cursor = storage.conn.execute("PRAGMA cache_size")
            assert cursor.fetchone()[0] == 20000
            
            storage.close()
        
        # Cleanup
        try:
            os.unlink(db_path)
            os.unlink(db_path + "-wal")
            os.unlink(db_path + "-shm")
        except:
            pass
    
    @pytest.mark.asyncio
    async def test_concurrent_reads(self, storage):
        """Test that multiple readers can access the database simultaneously."""
        # Store some test memories
        for i in range(5):
            memory = Memory(
                content=f"Test memory {i}",
                tags=["test"],
                memory_type="test"
            )
            await storage.store(memory)
        
        # Create multiple connections for reading
        readers = []
        for _ in range(3):
            conn = sqlite3.connect(storage.db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            readers.append(conn)
        
        # Perform concurrent reads
        results = []
        
        def read_count(conn):
            cursor = conn.execute("SELECT COUNT(*) FROM memories")
            return cursor.fetchone()[0]
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(read_count, conn) for conn in readers]
            results = [f.result() for f in futures]
        
        # All readers should see the same count
        assert all(r == 5 for r in results)
        
        # Cleanup
        for conn in readers:
            conn.close()
    
    @pytest.mark.asyncio
    async def test_retry_on_database_locked(self, storage):
        """Test that retry logic works when database is locked."""
        # Mock a locked database scenario
        original_execute = storage.conn.execute
        call_count = 0
        
        def mock_execute(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                raise sqlite3.OperationalError("database is locked")
            return original_execute(*args, **kwargs)
        
        with patch.object(storage.conn, 'execute', side_effect=mock_execute):
            memory = Memory(
                content="Test memory with retry",
                tags=["retry"],
                memory_type="test"
            )
            
            # Should succeed after retries
            success, msg = await storage.store(memory)
            assert success
            assert call_count > 1  # Verify retries happened
    
    @pytest.mark.asyncio
    async def test_exponential_backoff(self, storage):
        """Test that exponential backoff increases delay between retries."""
        delays = []
        
        async def mock_sleep(delay):
            delays.append(delay)
        
        # Create a failing operation that tracks retry delays
        def failing_operation():
            raise sqlite3.OperationalError("database is locked")
        
        with patch('asyncio.sleep', side_effect=mock_sleep):
            with pytest.raises(sqlite3.OperationalError):
                await storage._execute_with_retry(failing_operation, max_retries=3, initial_delay=0.1)
        
        # Check that delays increase exponentially (with jitter)
        assert len(delays) == 3
        for i in range(1, len(delays)):
            # Each delay should be roughly double the previous (accounting for jitter)
            assert delays[i] > delays[i-1] * 1.5
    
    @pytest.mark.asyncio
    async def test_non_retryable_errors(self, storage):
        """Test that non-lock errors are not retried."""
        call_count = 0
        
        def failing_operation():
            nonlocal call_count
            call_count += 1
            raise sqlite3.IntegrityError("UNIQUE constraint failed")
        
        with pytest.raises(sqlite3.IntegrityError):
            await storage._execute_with_retry(failing_operation)
        
        # Should not retry for non-lock errors
        assert call_count == 1
    
    @pytest.mark.asyncio
    async def test_wal_files_created(self, storage):
        """Test that WAL files are created when WAL mode is enabled."""
        # Store a memory to trigger WAL file creation
        memory = Memory(
            content="Test WAL file creation",
            tags=["wal"],
            memory_type="test"
        )
        await storage.store(memory)
        
        # Check that WAL files exist
        wal_path = storage.db_path + "-wal"
        shm_path = storage.db_path + "-shm"
        
        assert os.path.exists(wal_path), "WAL file should exist"
        assert os.path.exists(shm_path), "Shared memory file should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])