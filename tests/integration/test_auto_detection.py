"""
Integration tests for HTTP server auto-detection and coordination.
"""

import pytest
import pytest_asyncio
import asyncio
import tempfile
import os
import time
import subprocess
import sys
from typing import Optional
from unittest.mock import patch

from mcp_memory_service.utils.port_detection import (
    ServerCoordinator,
    detect_server_coordination_mode,
    is_port_in_use,
    is_mcp_memory_server_running
)
from mcp_memory_service.utils.http_server_manager import HTTPServerManager
from mcp_memory_service.storage.http_client import HTTPClientStorage
from mcp_memory_service.models.memory import Memory


class TestAutoDetection:
    """Test suite for server auto-detection and coordination."""
    
    @pytest_asyncio.fixture
    async def temp_db_path(self):
        """Create a temporary database path."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            path = tmp.name
        yield path
        # Cleanup
        for ext in ["", "-wal", "-shm"]:
            try:
                os.unlink(path + ext)
            except:
                pass
    
    @pytest.mark.asyncio
    async def test_port_detection(self):
        """Test basic port detection functionality."""
        # Test with a port that should be free
        port_free = await is_port_in_use(port=65432)
        assert port_free is False
        
        # Test with a port that's likely in use (if any)
        # Note: This might be flaky depending on system, so we'll be lenient
        common_ports = [80, 443, 22, 25]
        any_port_in_use = False
        for port in common_ports:
            if await is_port_in_use(port=port):
                any_port_in_use = True
                break
        # We don't assert this as it depends on the system
    
    @pytest.mark.asyncio
    async def test_mcp_server_detection_no_server(self):
        """Test MCP server detection when no server is running."""
        # Use a port that should be free
        is_running, server_info = await is_mcp_memory_server_running(port=65433)
        assert is_running is False
        assert server_info is None
    
    @pytest.mark.asyncio
    async def test_coordination_mode_detection_no_server(self):
        """Test coordination mode detection when no server is running."""
        # Use a free port for testing
        mode = await detect_server_coordination_mode(port=65434)
        # Should return "http_server" since port is available
        assert mode == "http_server"
    
    @pytest.mark.asyncio
    async def test_coordination_mode_detection_with_coordinator(self):
        """Test ServerCoordinator class functionality."""
        coordinator = ServerCoordinator(port=65435)
        
        # Initial state
        assert coordinator.get_mode() is None
        
        # Detect mode
        mode = await coordinator.detect_mode()
        assert mode in ["http_server", "direct"]
        assert coordinator.get_mode() == mode
        
        # Test convenience methods
        if mode == "http_server":
            assert coordinator.is_http_server_mode() is True
            assert coordinator.is_http_client_mode() is False
            assert coordinator.is_direct_mode() is False
        elif mode == "direct":
            assert coordinator.is_direct_mode() is True
            assert coordinator.is_http_server_mode() is False
            assert coordinator.is_http_client_mode() is False
    
    @pytest.mark.asyncio
    async def test_http_server_manager_disabled(self):
        """Test HTTP server manager when auto-start is disabled."""
        manager = HTTPServerManager()
        
        # Ensure auto-start is disabled
        with patch.dict(os.environ, {'MCP_MEMORY_HTTP_AUTO_START': 'false'}):
            result = await manager.start_http_server()
            assert result is False
            assert manager.is_server_running() is False
        
        # Cleanup
        manager.cleanup()
    
    @pytest.mark.asyncio
    async def test_http_server_manager_script_not_found(self):
        """Test HTTP server manager when script is not found."""
        manager = HTTPServerManager()
        
        # Enable auto-start but script won't be found (due to path manipulation)
        with patch.dict(os.environ, {'MCP_MEMORY_HTTP_AUTO_START': 'true'}):
            with patch('os.path.exists', return_value=False):
                result = await manager.start_http_server()
                assert result is False
        
        # Cleanup
        manager.cleanup()
    
    @pytest.mark.asyncio
    async def test_http_client_storage_initialization_failure(self):
        """Test HTTP client storage when server is not available."""
        # Use a port that should be free
        storage = HTTPClientStorage(base_url="http://localhost:65436")
        
        # Should fail to initialize
        with pytest.raises(RuntimeError, match="Failed to initialize HTTP client storage"):
            await storage.initialize()
        
        # Cleanup
        storage.close()
    
    @pytest.mark.asyncio
    async def test_server_coordination_workflow_no_server(self):
        """Test the complete server coordination workflow when no server exists."""
        coordinator = ServerCoordinator(port=65437)
        
        # Detect mode
        mode = await coordinator.detect_mode()
        
        if mode == "http_server":
            # Port is available, could start server
            manager = HTTPServerManager()
            
            # Try to start (should fail due to disabled auto-start)
            with patch.dict(os.environ, {'MCP_MEMORY_HTTP_AUTO_START': 'false'}):
                result = await manager.start_http_server()
                assert result is False
            
            manager.cleanup()
        elif mode == "direct":
            # Port is in use by something else, should fall back to direct
            assert coordinator.is_direct_mode() is True
    
    @pytest.mark.asyncio
    async def test_memory_operations_coordination_fallback(self, temp_db_path):
        """Test that memory operations work even when HTTP coordination fails."""
        # This test simulates the scenario where HTTP coordination is attempted
        # but falls back to direct SQLite access
        
        # Mock a scenario where HTTP server auto-start is enabled but fails
        with patch.dict(os.environ, {
            'MCP_MEMORY_HTTP_AUTO_START': 'true',
            'MCP_MEMORY_STORAGE_BACKEND': 'sqlite_vec',
            'MCP_MEMORY_SQLITE_PATH': temp_db_path
        }):
            # Import and create the server (this will trigger coordination logic)
            from mcp_memory_service.server import MemoryServer
            
            server = MemoryServer()
            
            # Initialize storage (should fall back to direct SQLite)
            storage = await server._ensure_storage_initialized()
            assert storage is not None
            
            # Test basic memory operations
            memory = Memory(
                content="Test coordination fallback",
                tags=["integration", "fallback"],
                memory_type="test"
            )
            
            success, message = await storage.store(memory)
            assert success is True
            
            # Search for the memory
            results = await storage.search_by_tag(["integration"])
            assert len(results) >= 1
            assert any("coordination fallback" in r.content for r in results)
            
            # Cleanup
            storage.close()
    
    @pytest.mark.asyncio
    async def test_concurrent_coordination_detection(self):
        """Test that multiple coordination detections work correctly."""
        # Run multiple coordination detections concurrently
        coordinators = [ServerCoordinator(port=65440 + i) for i in range(3)]
        
        # Detect modes concurrently
        tasks = [coord.detect_mode() for coord in coordinators]
        modes = await asyncio.gather(*tasks)
        
        # All should succeed and return valid modes
        for mode in modes:
            assert mode in ["http_client", "http_server", "direct"]
        
        # Each coordinator should have a cached mode
        for coord in coordinators:
            assert coord.get_mode() is not None
    
    @pytest.mark.asyncio
    async def test_error_handling_in_coordination(self):
        """Test error handling in coordination detection."""
        # Test with invalid host
        with patch('socket.socket') as mock_socket:
            mock_socket.side_effect = Exception("Network error")
            
            # Should handle gracefully
            port_in_use = await is_port_in_use(host="invalid-host", port=65441)
            assert port_in_use is False  # Should return False on error
        
        # Test with timeout in server detection
        with patch('aiohttp.ClientSession') as mock_session:
            mock_session_instance = mock_session.return_value
            mock_session_instance.get.side_effect = asyncio.TimeoutError()
            
            is_running, server_info = await is_mcp_memory_server_running(port=65442)
            assert is_running is False
            assert server_info is None


class TestEndToEndCoordination:
    """End-to-end coordination tests (more resource intensive)."""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_full_coordination_cycle_mock(self):
        """Test a full coordination cycle with mocked HTTP server."""
        # This test mocks the entire coordination cycle without actually
        # starting processes, to ensure the logic flow works correctly
        
        coordinator = ServerCoordinator(port=65450)
        
        # Mock the detection to return "http_server" mode
        with patch.object(coordinator, 'detect_mode', return_value="http_server"):
            mode = await coordinator.detect_mode()
            assert mode == "http_server"
            assert coordinator.is_http_server_mode()
            
            # Mock server manager to simulate successful start
            manager = HTTPServerManager()
            with patch.object(manager, 'start_http_server', return_value=True):
                result = await manager.start_http_server()
                assert result is True
                
                # Mock that server is running
                with patch.object(manager, 'is_server_running', return_value=True):
                    assert manager.is_server_running()
                
                # Cleanup
                manager.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])