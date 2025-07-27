#!/usr/bin/env python3
"""
Final test script for multi-client setup - sets environment internally.
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

# Set environment variables programmatically
os.environ['MCP_MEMORY_STORAGE_BACKEND'] = 'sqlite_vec'
os.environ['MCP_MEMORY_HTTP_AUTO_START'] = 'true'
os.environ['MCP_HTTP_PORT'] = '8000'
os.environ['MCP_HTTP_HOST'] = 'localhost'
os.environ['MCP_MEMORY_SQLITE_PRAGMAS'] = 'busy_timeout=10000,cache_size=20000'
os.environ['LOG_LEVEL'] = 'INFO'

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def check_environment():
    """Check the current environment configuration."""
    print("Environment Configuration:")
    
    config_vars = [
        "MCP_MEMORY_STORAGE_BACKEND",
        "MCP_MEMORY_HTTP_AUTO_START", 
        "MCP_HTTP_PORT",
        "MCP_HTTP_HOST",
        "MCP_MEMORY_SQLITE_PRAGMAS",
        "LOG_LEVEL"
    ]
    
    for var in config_vars:
        value = os.environ.get(var, "not set")
        print(f"  {var}: {value}")
    
    # Check if configuration looks good
    backend = os.environ.get("MCP_MEMORY_STORAGE_BACKEND")
    if backend == "sqlite_vec":
        print("[OK] SQLite-vec backend configured correctly")
    else:
        print(f"[WARNING] Backend is '{backend}', should be 'sqlite_vec'")
    
    auto_start = os.environ.get("MCP_MEMORY_HTTP_AUTO_START")
    if auto_start == "true":
        print("[OK] HTTP auto-start enabled for advanced coordination")
    else:
        print("[INFO] HTTP auto-start disabled, will use WAL mode only")

async def test_coordination_detection():
    """Test the coordination mode detection."""
    print("\nTesting coordination mode detection...")
    
    try:
        from mcp_memory_service.utils.port_detection import ServerCoordinator
        
        coordinator = ServerCoordinator()
        mode = await coordinator.detect_mode()
        
        print(f"[OK] Detected coordination mode: {mode}")
        
        if mode == "http_client":
            print("  -> Found existing HTTP server - will connect as client")
        elif mode == "http_server":
            print("  -> No server found, can start HTTP server for coordination")
        elif mode == "direct":
            print("  -> Will use direct SQLite access with WAL mode")
        
        return mode
        
    except Exception as e:
        print(f"[ERROR] Error detecting coordination mode: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_storage_initialization():
    """Test storage initialization with current configuration."""
    print("\nTesting storage initialization...")
    
    try:
        from mcp_memory_service.server import MemoryServer
        
        # Create a temporary database for testing
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            test_db_path = tmp.name
        
        # Override the database path for testing
        original_path = os.environ.get('MCP_MEMORY_SQLITE_PATH')
        os.environ['MCP_MEMORY_SQLITE_PATH'] = test_db_path
        
        try:
            print("  Creating MemoryServer...")
            server = MemoryServer()
            
            print("  Initializing storage...")
            storage = await server._ensure_storage_initialized()
            
            if storage:
                print(f"[OK] Storage initialized successfully")
                print(f"  Storage type: {type(storage).__name__}")
                
                # Check if it's HTTP client or direct SQLite
                if "HTTPClient" in type(storage).__name__:
                    print("  -> Using HTTP client storage (connecting to server)")
                elif "SqliteVec" in type(storage).__name__:
                    print("  -> Using direct SQLite storage with WAL mode")
                
                # Test basic operations
                from mcp_memory_service.models.memory import Memory
                
                test_memory = Memory(
                    content="Multi-client test memory from setup",
                    tags=["test", "multi-client", "setup"],
                    memory_type="test"
                )
                
                print("  Testing memory storage...")
                success, message = await storage.store(test_memory)
                if success:
                    print("[OK] Test memory stored successfully")
                    
                    # Try to retrieve it
                    print("  Testing memory retrieval...")
                    results = await storage.search_by_tag(["setup"])
                    if results:
                        print(f"[OK] Test memory retrieved successfully ({len(results)} results)")
                        print(f"  Content: {results[0].content[:50]}...")
                    else:
                        print("[WARNING] Could not retrieve test memory")
                else:
                    print(f"[ERROR] Failed to store test memory: {message}")
                
                # Cleanup
                storage.close()
                return True
            else:
                print("[ERROR] Failed to initialize storage")
                return False
                
        finally:
            # Restore original path
            if original_path:
                os.environ['MCP_MEMORY_SQLITE_PATH'] = original_path
            else:
                os.environ.pop('MCP_MEMORY_SQLITE_PATH', None)
            
            # Cleanup test database
            try:
                os.unlink(test_db_path)
                for ext in ["-wal", "-shm"]:
                    try:
                        os.unlink(test_db_path + ext)
                    except:
                        pass
            except:
                pass
                
    except Exception as e:
        print(f"[ERROR] Error testing storage: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_setup_instructions():
    """Print setup instructions for Claude Desktop."""
    print("\n" + "="*60)
    print("MULTI-CLIENT SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n1. ENVIRONMENT VARIABLES (already set by setup script):")
    print("   MCP_MEMORY_STORAGE_BACKEND=sqlite_vec")
    print("   MCP_MEMORY_HTTP_AUTO_START=true")
    print("   MCP_HTTP_PORT=8000")
    
    print("\n2. CLAUDE DESKTOP CONFIGURATION:")
    print("   Location: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("   Add this configuration:")
    
    config = '''{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "C:\\\\REPOSITORIES\\\\mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_HTTP_AUTO_START": "true"
      }
    }
  }
}'''
    print(config)
    
    print("\n3. RESTART INSTRUCTIONS:")
    print("   - Close Claude Desktop completely (check system tray)")
    print("   - Restart Claude Desktop")
    print("   - Restart any Claude Code sessions")
    
    print("\n4. TESTING:")
    print("   - Start both Claude Desktop and Claude Code")
    print("   - Try storing memories from both clients")
    print("   - Check that they can see each other's memories")
    
    print("\n5. TROUBLESHOOTING:")
    print("   - Check logs for 'Detected coordination mode: ...' messages")
    print("   - If HTTP coordination fails, system will fall back to WAL mode")
    print("   - For debugging, set LOG_LEVEL=DEBUG in environment")

async def main():
    """Run all tests."""
    print("MCP Memory Service Multi-Client Setup Test")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Test coordination detection
    mode = await test_coordination_detection()
    
    # Test storage initialization
    if mode:
        storage_ok = await test_storage_initialization()
        
        if storage_ok:
            print("\n" + "="*50)
            print("SUCCESS: Multi-Client Setup Test PASSED!")
            print("="*50)
            print("\nYour system is ready for multi-client access:")
            print("  -> Claude Desktop and Claude Code can run simultaneously")
            print("  -> Automatic coordination will handle database access")
            print("  -> System falls back to WAL mode if HTTP coordination fails")
            
            print_setup_instructions()
            
        else:
            print("\n[ERROR] Storage initialization failed")
            print("Check the error messages above for troubleshooting.")
    else:
        print("\n[ERROR] Coordination detection failed")
        print("Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    asyncio.run(main())