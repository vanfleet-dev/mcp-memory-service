#!/usr/bin/env python3
"""
Minimal FastAPI MCP Server Test
Tests the MCP protocol integration without heavy dependencies.
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Add src to path
sys.path.insert(0, 'src')

from mcp.server.fastmcp import FastMCP, Context

# Create minimal FastAPI MCP server
mcp = FastMCP("MCP Memory Service Test")

# Mock storage for testing
mock_memories = []
next_id = 1

@mcp.tool()
async def store_memory(
    content: str,
    ctx: Context,
    tags: Optional[List[str]] = None,
    memory_type: str = "note",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Union[bool, str]]:
    """Store a new memory with content and optional metadata."""
    global next_id
    
    memory = {
        "id": next_id,
        "content": content,
        "tags": tags or [],
        "memory_type": memory_type,
        "metadata": metadata or {},
        "content_hash": f"hash_{next_id}"
    }
    
    mock_memories.append(memory)
    next_id += 1
    
    return {
        "success": True,
        "message": f"Stored memory: {content[:50]}...",
        "content_hash": memory["content_hash"]
    }

@mcp.tool()
async def retrieve_memory(
    query: str,
    ctx: Context,
    n_results: int = 5,
    min_similarity: float = 0.0
) -> Dict[str, Any]:
    """Retrieve memories based on query (mock implementation)."""
    # Simple keyword matching for testing
    results = []
    for memory in mock_memories:
        if query.lower() in memory["content"].lower():
            results.append({
                "content": memory["content"],
                "content_hash": memory["content_hash"],
                "tags": memory["tags"],
                "memory_type": memory["memory_type"],
                "similarity_score": 0.8  # Mock score
            })
    
    return {
        "memories": results[:n_results],
        "query": query,
        "total_results": len(results)
    }

@mcp.tool()
async def search_by_tag(
    tags: Union[str, List[str]],
    ctx: Context,
    match_all: bool = False
) -> Dict[str, Any]:
    """Search memories by tags."""
    if isinstance(tags, str):
        tags = [tags]
    
    results = []
    for memory in mock_memories:
        memory_tags = memory["tags"]
        
        if match_all:
            # All tags must be present
            if all(tag in memory_tags for tag in tags):
                results.append({
                    "content": memory["content"],
                    "content_hash": memory["content_hash"],
                    "tags": memory["tags"],
                    "memory_type": memory["memory_type"]
                })
        else:
            # Any tag must be present
            if any(tag in memory_tags for tag in tags):
                results.append({
                    "content": memory["content"],
                    "content_hash": memory["content_hash"],
                    "tags": memory["tags"],
                    "memory_type": memory["memory_type"]
                })
    
    return {
        "memories": results,
        "search_tags": tags,
        "match_all": match_all,
        "total_results": len(results)
    }

@mcp.tool()
async def delete_memory(
    content_hash: str,
    ctx: Context
) -> Dict[str, Union[bool, str]]:
    """Delete a specific memory by its content hash."""
    global mock_memories
    
    for i, memory in enumerate(mock_memories):
        if memory["content_hash"] == content_hash:
            deleted_memory = mock_memories.pop(i)
            return {
                "success": True,
                "message": f"Deleted memory: {deleted_memory['content'][:50]}...",
                "content_hash": content_hash
            }
    
    return {
        "success": False,
        "message": f"Memory with hash {content_hash} not found",
        "content_hash": content_hash
    }

@mcp.tool()
async def check_database_health(ctx: Context) -> Dict[str, Any]:
    """Check the health and status of the memory database."""
    return {
        "status": "healthy",
        "backend": "MockStorage",
        "statistics": {
            "total_memories": len(mock_memories),
            "total_tags": len(set(tag for memory in mock_memories for tag in memory["tags"])),
            "storage_size": "minimal",
            "last_backup": "never"
        },
        "timestamp": "2025-08-03T06:00:00Z"
    }

def main():
    """Main entry point for testing."""
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    host = os.getenv("MCP_SERVER_HOST", "localhost")
    
    print(f"🚀 Starting MCP Memory Service Test Server")
    print(f"📍 Address: {host}:{port}")
    print(f"🔧 Tools: store_memory, retrieve_memory, search_by_tag, delete_memory, check_database_health")
    print(f"💾 Storage: Mock (in-memory)")
    print(f"🔗 Transport: streamable-http")
    print(f"📜 Version: 4.0.0-alpha.1")
    print()
    
    try:
        # Run server with streamable HTTP transport
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()