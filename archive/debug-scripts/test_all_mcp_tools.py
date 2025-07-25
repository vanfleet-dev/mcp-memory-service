#!/usr/bin/env python3
"""
Test all MCP tools directly using the server
"""

import asyncio
import json
import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_memory_service.server import main as server_main

async def test_direct_operations():
    """Test operations directly on the server"""
    # Initialize server components
    from mcp_memory_service.server import MemoryServer
    
    server = MemoryServer()
    
    # Test results
    results = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tests": {}
    }
    
    print("Testing direct server operations...")
    
    # Test 1: Store a memory
    print("\n1. Testing store_memory...")
    try:
        test_content = f"Test memory - {datetime.datetime.now()}"
        # Note: Direct server testing would require setting up the full MCP context
        results["tests"]["store_memory"] = {"status": "requires_mcp_context"}
    except Exception as e:
        results["tests"]["store_memory"] = {"status": "error", "error": str(e)}
    
    # Test 2: Health check
    print("\n2. Testing health check...")
    try:
        from mcp_memory_service.services.health_service import HealthService
        health_service = HealthService()
        await health_service.initialize()
        health_status = await health_service.get_health_status()
        results["tests"]["health_check"] = {
            "status": "success",
            "result": health_status
        }
    except Exception as e:
        results["tests"]["health_check"] = {"status": "error", "error": str(e)}
    
    return results

def check_installation():
    """Check if installation and dependencies are working"""
    results = {}
    
    # Check imports
    print("\nChecking imports...")
    try:
        import mcp_memory_service
        results["mcp_memory_service"] = "OK"
    except ImportError as e:
        results["mcp_memory_service"] = f"Failed: {e}"
    
    try:
        import chromadb
        results["chromadb"] = "OK"
    except ImportError as e:
        results["chromadb"] = f"Failed: {e}"
    
    try:
        import sentence_transformers
        results["sentence_transformers"] = "OK"
    except ImportError as e:
        results["sentence_transformers"] = f"Failed: {e}"
    
    # Check paths
    print("\nChecking paths...")
    from mcp_memory_service.config import Config
    config = Config()
    
    results["paths"] = {
        "chroma_path": str(config.chroma_path),
        "chroma_exists": config.chroma_path.exists(),
        "backups_path": str(config.backups_path),
        "backups_exists": config.backups_path.exists()
    }
    
    return results

async def main():
    """Run all tests"""
    print("=" * 60)
    print("MCP Memory Service - Direct Testing")
    print("=" * 60)
    
    # Check installation
    print("\n### Installation Check ###")
    install_results = check_installation()
    for key, value in install_results.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    # Test direct operations
    print("\n### Direct Operations Test ###")
    test_results = await test_direct_operations()
    
    # Save results
    all_results = {
        "installation": install_results,
        "operations": test_results
    }
    
    with open("direct_test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n\nResults saved to: direct_test_results.json")

if __name__ == "__main__":
    asyncio.run(main())