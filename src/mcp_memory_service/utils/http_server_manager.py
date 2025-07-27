"""
HTTP server management utilities for auto-starting coordination servers.
"""

import asyncio
import logging
import os
import subprocess
import sys
import signal
from typing import Optional
from ..config import HTTP_HOST, HTTP_PORT

logger = logging.getLogger(__name__)


class HTTPServerManager:
    """Manager for auto-starting and stopping HTTP coordination servers."""
    
    def __init__(self):
        self.server_process: Optional[subprocess.Popen] = None
        self.server_task: Optional[asyncio.Task] = None
    
    async def start_http_server(self) -> bool:
        """
        Start the HTTP server in a subprocess for multi-client coordination.
        
        Returns:
            True if server started successfully, False otherwise
        """
        try:
            # Check if auto-start is enabled
            auto_start = os.getenv('MCP_MEMORY_HTTP_AUTO_START', 'false').lower() == 'true'
            if not auto_start:
                logger.info("HTTP server auto-start disabled via MCP_MEMORY_HTTP_AUTO_START")
                return False
            
            # Prepare environment for the HTTP server
            env = os.environ.copy()
            env.update({
                'MCP_HTTP_ENABLED': 'true',
                'MCP_MEMORY_STORAGE_BACKEND': 'sqlite_vec',
                'LOG_LEVEL': 'INFO'
            })
            
            # Get the script path
            script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            http_script = os.path.join(script_dir, 'scripts', 'run_http_server.py')
            
            if not os.path.exists(http_script):
                logger.error(f"HTTP server script not found: {http_script}")
                return False
            
            # Start the HTTP server process
            logger.info(f"Starting HTTP server subprocess: {http_script}")
            
            self.server_process = subprocess.Popen(
                [sys.executable, http_script],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True  # Prevent signal propagation
            )
            
            # Wait a moment for the server to start
            await asyncio.sleep(2.0)
            
            # Check if the process is still running
            if self.server_process.poll() is None:
                logger.info(f"HTTP server started successfully (PID: {self.server_process.pid})")
                return True
            else:
                stdout, stderr = self.server_process.communicate()
                logger.error(f"HTTP server failed to start: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to start HTTP server: {str(e)}")
            return False
    
    def stop_http_server(self):
        """Stop the HTTP server subprocess."""
        if self.server_process:
            try:
                logger.info(f"Stopping HTTP server (PID: {self.server_process.pid})")
                
                # Try graceful shutdown first
                self.server_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.server_process.wait(timeout=5)
                    logger.info("HTTP server stopped gracefully")
                except subprocess.TimeoutExpired:
                    logger.warning("HTTP server didn't stop gracefully, forcing shutdown")
                    self.server_process.kill()
                    self.server_process.wait()
                    logger.info("HTTP server force stopped")
                    
            except Exception as e:
                logger.error(f"Error stopping HTTP server: {str(e)}")
            finally:
                self.server_process = None
    
    def is_server_running(self) -> bool:
        """Check if the managed HTTP server is running."""
        return self.server_process is not None and self.server_process.poll() is None
    
    async def start_embedded_server(self) -> bool:
        """
        Start the HTTP server as an embedded task (alternative to subprocess).
        
        This approach runs the server in the same process, which can be useful
        for development but may not be ideal for production.
        """
        try:
            # Check if auto-start is enabled
            auto_start = os.getenv('MCP_MEMORY_HTTP_AUTO_START', 'false').lower() == 'true'
            if not auto_start:
                logger.info("HTTP server auto-start disabled")
                return False
            
            # Import the FastAPI app
            from ..web.app import app
            import uvicorn
            
            # Configure uvicorn
            config = uvicorn.Config(
                app,
                host=HTTP_HOST,
                port=HTTP_PORT,
                log_level="info",
                access_log=False  # Reduce noise
            )
            
            # Create and start the server in a background task
            server = uvicorn.Server(config)
            
            async def run_server():
                try:
                    await server.serve()
                except Exception as e:
                    logger.error(f"Embedded HTTP server error: {str(e)}")
            
            self.server_task = asyncio.create_task(run_server())
            
            # Wait a moment for the server to start
            await asyncio.sleep(1.0)
            
            logger.info(f"Embedded HTTP server started on {HTTP_HOST}:{HTTP_PORT}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start embedded HTTP server: {str(e)}")
            return False
    
    def stop_embedded_server(self):
        """Stop the embedded HTTP server task."""
        if self.server_task and not self.server_task.done():
            logger.info("Stopping embedded HTTP server")
            self.server_task.cancel()
            self.server_task = None
    
    def cleanup(self):
        """Clean up all managed server resources."""
        self.stop_http_server()
        self.stop_embedded_server()


# Global server manager instance
_server_manager: Optional[HTTPServerManager] = None


def get_server_manager() -> HTTPServerManager:
    """Get the global server manager instance."""
    global _server_manager
    if _server_manager is None:
        _server_manager = HTTPServerManager()
    return _server_manager


async def auto_start_http_server_if_needed() -> bool:
    """
    Auto-start HTTP server if coordination mode suggests it's needed.
    
    Returns:
        True if server was started or already running, False otherwise
    """
    from .port_detection import detect_server_coordination_mode
    
    # Check current coordination mode
    mode = await detect_server_coordination_mode()
    
    if mode == "http_server":
        logger.info("Coordination mode suggests starting HTTP server")
        manager = get_server_manager()
        
        # Try subprocess approach first, fall back to embedded
        if await manager.start_http_server():
            return True
        else:
            logger.warning("Subprocess HTTP server failed, trying embedded approach")
            return await manager.start_embedded_server()
    else:
        logger.info(f"Coordination mode '{mode}' doesn't require HTTP server startup")
        return mode == "http_client"  # Return True if connecting to existing server