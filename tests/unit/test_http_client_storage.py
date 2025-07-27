"""
Unit tests for HTTPClientStorage adapter.
"""

import pytest
import pytest_asyncio
import aiohttp
from unittest.mock import AsyncMock, MagicMock, patch
import json

from mcp_memory_service.storage.http_client import HTTPClientStorage
from mcp_memory_service.models.memory import Memory, MemoryQueryResult


class TestHTTPClientStorage:
    """Test suite for HTTPClientStorage adapter."""
    
    @pytest_asyncio.fixture
    async def http_storage(self):
        """Create an HTTPClientStorage instance for testing."""
        storage = HTTPClientStorage(base_url="http://test-server:8000")
        yield storage
        # Cleanup
        if storage.session:
            await storage.session.close()
    
    @pytest_asyncio.fixture
    async def mock_session(self):
        """Create a mock aiohttp session."""
        session = AsyncMock(spec=aiohttp.ClientSession)
        return session
    
    @pytest.mark.asyncio
    async def test_initialization_success(self, http_storage):
        """Test successful initialization."""
        # Mock the health check response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "service": "mcp-memory-service",
            "version": "0.2.2",
            "status": "healthy"
        })
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value = mock_session
            mock_session.get.return_value = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
            
            await http_storage.initialize()
            
            assert http_storage._initialized is True
            assert http_storage.session is not None
    
    @pytest.mark.asyncio
    async def test_initialization_failure(self, http_storage):
        """Test initialization failure when server is not available."""
        mock_response = AsyncMock()
        mock_response.status = 500
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_session = AsyncMock()
            mock_session_class.return_value = mock_session
            mock_session.get.return_value = AsyncMock()
            mock_session.get.return_value.__aenter__ = AsyncMock(return_value=mock_response)
            mock_session.get.return_value.__aexit__ = AsyncMock(return_value=None)
            
            with pytest.raises(RuntimeError, match="Failed to initialize HTTP client storage"):
                await http_storage.initialize()
            
            assert http_storage._initialized is False
    
    @pytest.mark.asyncio
    async def test_store_memory_success(self, http_storage):
        """Test successful memory storage."""
        memory = Memory(
            content="Test memory content",
            tags=["test", "unit"],
            memory_type="test",
            metadata={"source": "unit_test"}
        )
        
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status = 201
        mock_response.json = AsyncMock(return_value={
            "content_hash": "abc123",
            "message": "Memory stored successfully"
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.post.return_value.__aenter__.return_value = mock_response
        
        success, message = await http_storage.store(memory)
        
        assert success is True
        assert "abc123" in message
        
        # Verify the request was made correctly
        http_storage.session.post.assert_called_once()
        call_args = http_storage.session.post.call_args
        assert call_args[0][0] == "http://test-server:8000/api/memories"
        
        # Check the payload
        payload = call_args[1]["json"]
        assert payload["content"] == "Test memory content"
        assert payload["tags"] == ["test", "unit"]
        assert payload["memory_type"] == "test"
    
    @pytest.mark.asyncio
    async def test_store_memory_failure(self, http_storage):
        """Test memory storage failure."""
        memory = Memory(content="Test content")
        
        # Mock error response
        mock_response = AsyncMock()
        mock_response.status = 400
        mock_response.json = AsyncMock(return_value={
            "detail": "Invalid memory content"
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.post.return_value.__aenter__.return_value = mock_response
        
        success, message = await http_storage.store(memory)
        
        assert success is False
        assert "Invalid memory content" in message
    
    @pytest.mark.asyncio
    async def test_retrieve_memories_success(self, http_storage):
        """Test successful memory retrieval."""
        # Mock successful search response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "results": [
                {
                    "memory": {
                        "content": "Test memory 1",
                        "content_hash": "hash1",
                        "tags": ["test"],
                        "memory_type": "test",
                        "metadata": {},
                        "created_at": 1609459200.0,
                        "updated_at": 1609459200.0,
                        "created_at_iso": "2021-01-01T00:00:00Z",
                        "updated_at_iso": "2021-01-01T00:00:00Z"
                    },
                    "similarity_score": 0.95
                },
                {
                    "memory": {
                        "content": "Test memory 2",
                        "content_hash": "hash2",
                        "tags": ["test"],
                        "memory_type": "test",
                        "metadata": {},
                        "created_at": 1609459200.0,
                        "updated_at": 1609459200.0,
                        "created_at_iso": "2021-01-01T00:00:00Z",
                        "updated_at_iso": "2021-01-01T00:00:00Z"
                    },
                    "similarity_score": 0.85
                }
            ]
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.post.return_value.__aenter__.return_value = mock_response
        
        results = await http_storage.retrieve("test query", n_results=5)
        
        assert len(results) == 2
        assert isinstance(results[0], MemoryQueryResult)
        assert results[0].memory.content == "Test memory 1"
        assert results[0].relevance_score == 0.95
        assert results[1].memory.content == "Test memory 2"
        assert results[1].relevance_score == 0.85
        
        # Verify the request
        http_storage.session.post.assert_called_once()
        call_args = http_storage.session.post.call_args
        assert call_args[0][0] == "http://test-server:8000/api/search/semantic"
        
        payload = call_args[1]["json"]
        assert payload["query"] == "test query"
        assert payload["n_results"] == 5
    
    @pytest.mark.asyncio
    async def test_search_by_tag_success(self, http_storage):
        """Test successful tag-based search."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "memories": [
                {
                    "content": "Tagged memory",
                    "content_hash": "hash1",
                    "tags": ["important", "work"],
                    "memory_type": "note",
                    "metadata": {"priority": "high"},
                    "created_at": 1609459200.0,
                    "updated_at": 1609459200.0,
                    "created_at_iso": "2021-01-01T00:00:00Z",
                    "updated_at_iso": "2021-01-01T00:00:00Z"
                }
            ]
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.post.return_value.__aenter__.return_value = mock_response
        
        results = await http_storage.search_by_tag(["important", "work"])
        
        assert len(results) == 1
        assert isinstance(results[0], Memory)
        assert results[0].content == "Tagged memory"
        assert results[0].tags == ["important", "work"]
        assert results[0].metadata == {"priority": "high"}
        
        # Verify the request
        call_args = http_storage.session.post.call_args
        payload = call_args[1]["json"]
        assert payload["tags"] == ["important", "work"]
        assert payload["match_all"] is False
    
    @pytest.mark.asyncio
    async def test_delete_memory_success(self, http_storage):
        """Test successful memory deletion."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "message": "Memory deleted successfully"
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.delete.return_value.__aenter__.return_value = mock_response
        
        success, message = await http_storage.delete("test_hash")
        
        assert success is True
        assert "deleted successfully" in message
        
        # Verify the request
        http_storage.session.delete.assert_called_once()
        call_args = http_storage.session.delete.call_args
        assert call_args[0][0] == "http://test-server:8000/api/memories/test_hash"
    
    @pytest.mark.asyncio
    async def test_delete_memory_not_found(self, http_storage):
        """Test memory deletion when memory not found."""
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.json = AsyncMock(return_value={
            "detail": "Memory not found"
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.delete.return_value.__aenter__.return_value = mock_response
        
        success, message = await http_storage.delete("nonexistent_hash")
        
        assert success is False
        assert "not found" in message
    
    @pytest.mark.asyncio
    async def test_operations_without_initialization(self, http_storage):
        """Test that operations fail gracefully when not initialized."""
        # Ensure not initialized
        http_storage._initialized = False
        http_storage.session = None
        
        # Test store
        memory = Memory(content="Test")
        success, message = await http_storage.store(memory)
        assert success is False
        assert "not initialized" in message
        
        # Test retrieve
        results = await http_storage.retrieve("test")
        assert len(results) == 0
        
        # Test search by tag
        results = await http_storage.search_by_tag(["test"])
        assert len(results) == 0
        
        # Test delete
        success, message = await http_storage.delete("hash")
        assert success is False
        assert "not initialized" in message
    
    @pytest.mark.asyncio
    async def test_recall_memories(self, http_storage):
        """Test memory recall with time filtering."""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={
            "results": [
                {
                    "memory": {
                        "content": "Recent memory",
                        "content_hash": "hash1",
                        "tags": ["recent"],
                        "memory_type": "note",
                        "metadata": {},
                        "created_at": 1609459200.0,
                        "updated_at": 1609459200.0,
                        "created_at_iso": "2021-01-01T00:00:00Z",
                        "updated_at_iso": "2021-01-01T00:00:00Z"
                    },
                    "similarity_score": 0.9
                }
            ]
        })
        
        http_storage._initialized = True
        http_storage.session = AsyncMock()
        http_storage.session.post.return_value.__aenter__.return_value = mock_response
        
        results = await http_storage.recall(
            query="recent memories",
            n_results=10,
            start_timestamp=1609459200.0,
            end_timestamp=1609545600.0
        )
        
        assert len(results) == 1
        assert isinstance(results[0], MemoryQueryResult)
        assert results[0].memory.content == "Recent memory"
        assert results[0].debug_info["time_filtered"] is True
    
    @pytest.mark.asyncio
    async def test_get_stats(self, http_storage):
        """Test getting storage statistics."""
        stats = http_storage.get_stats()
        
        assert stats["backend"] == "http_client"
        assert stats["server"] == "http://test-server:8000"
        assert "initialized" in stats
    
    @pytest.mark.asyncio
    async def test_unsupported_operations(self, http_storage):
        """Test operations that are not supported via HTTP client."""
        # delete_by_tag should return safety message
        count, message = await http_storage.delete_by_tag("test")
        assert count == 0
        assert "safety" in message.lower()
        
        # cleanup_duplicates should return server-side message
        count, message = await http_storage.cleanup_duplicates()
        assert count == 0
        assert "server side" in message.lower()
        
        # update_memory_metadata should return not supported message
        success, message = await http_storage.update_memory_metadata("hash", {})
        assert success is False
        assert "not supported" in message.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])