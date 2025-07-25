#!/usr/bin/env python3
"""
Run the MCP Memory Service HTTP server.

This script starts the FastAPI server with uvicorn.
"""

import os
import sys
import logging
import asyncio

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

def main():
    """Run the HTTP server."""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set default environment variables for testing
    os.environ.setdefault('MCP_HTTP_ENABLED', 'true')
    os.environ.setdefault('MCP_MEMORY_STORAGE_BACKEND', 'sqlite_vec')
    os.environ.setdefault('LOG_LEVEL', 'INFO')
    
    try:
        import uvicorn
        from mcp_memory_service.web.app import app
        from mcp_memory_service.config import HTTP_HOST, HTTP_PORT
        
        print(f"Starting MCP Memory Service HTTP server on {HTTP_HOST}:{HTTP_PORT}")
        print(f"Dashboard: http://{HTTP_HOST if HTTP_HOST != '0.0.0.0' else 'localhost'}:{HTTP_PORT}")
        print(f"API Docs: http://{HTTP_HOST if HTTP_HOST != '0.0.0.0' else 'localhost'}:{HTTP_PORT}/api/docs")
        print("Press Ctrl+C to stop")
        
        uvicorn.run(
            app,
            host=HTTP_HOST,
            port=HTTP_PORT,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        print(f"Error: Missing dependencies. Please run 'python install.py' first.")
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()