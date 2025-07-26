# Enable Multi-Client Access for SQLite-vec Backend

## Problem Description

When using the SQLite-vec backend, it's not possible to run the MCP Memory Service simultaneously in multiple clients (e.g., Claude Desktop and Claude Code). This limitation doesn't exist with the ChromaDB backend, which previously allowed concurrent access from multiple Claude instances.

### Current Behavior
- With ChromaDB: Multiple Claude instances could access the same memory service
- With SQLite-vec: Only one client can connect at a time; attempting to use in Claude Code while Claude Desktop is running fails

### Expected Behavior
Users should be able to access their memory service from multiple Claude instances simultaneously, regardless of the storage backend.

## Technical Analysis

### Why ChromaDB Worked
ChromaDB uses a client-server architecture:
- ChromaDB runs as a persistent background service/daemon
- Each MCP server instance acts as a client connecting to the ChromaDB service
- No file locking issues as clients communicate via API, not direct file access
- Multiple clients can read/write simultaneously through the service layer

### Why SQLite-vec Doesn't Work
SQLite-vec uses direct file access:
- Each MCP server instance opens the SQLite database file directly
- SQLite implements file-level locking to prevent corruption
- Default mode allows only one writer at a time
- Multiple processes attempting to access the same file encounter locking conflicts

## Proposed Solutions

### 1. Short-term Fix: Enable SQLite WAL Mode
Modify the SQLite-vec storage backend to use Write-Ahead Logging (WAL):

```python
# In sqlite_vec.py initialize method
self.conn.execute("PRAGMA journal_mode=WAL")  # Enable multiple readers + one writer
self.conn.execute("PRAGMA busy_timeout=5000")  # Handle concurrent access gracefully
```

Benefits:
- Allows multiple simultaneous readers
- One writer at a time (sufficient for most use cases)
- Minimal code changes required
- Better performance for concurrent access

### 2. Medium-term: Shared Service Architecture
Implement a hybrid approach where:
- A single HTTP server manages all SQLite-vec operations
- MCP stdio servers act as thin clients forwarding requests to HTTP
- Similar to the HTTP/SSE feature but used internally

Options:
- **Option A**: Auto-start HTTP server when first MCP client launches
- **Option B**: Use Unix domain sockets (Linux/Mac) or named pipes (Windows) for IPC
- **Option C**: Implement a lightweight gRPC service

### 3. Long-term: Full Client-Server Architecture
Redesign the SQLite-vec backend to mirror ChromaDB's architecture:
- Separate daemon process managing the SQLite database
- MCP servers connect as clients
- Implement proper connection pooling and transaction management
- Support for distributed locking and concurrent operations

## Implementation Plan

### Phase 1: WAL Mode (1-2 days)
1. Modify `sqlite_vec.py` to enable WAL mode
2. Add connection retry logic with exponential backoff
3. Implement read-only connections for search operations
4. Test concurrent access scenarios

### Phase 2: Claude Code Integration (2-3 days)
1. Create wrapper script that detects running instances
2. If HTTP server exists, connect as client
3. If not, start new server instance
4. Document configuration for Claude Code settings

### Phase 3: Shared Service (1 week)
1. Design internal API for shared access
2. Implement service discovery mechanism
3. Create thin MCP client wrapper
4. Ensure backward compatibility

## Benefits
- Restores multi-client functionality lost in ChromaDB → SQLite-vec migration
- Maintains SQLite-vec's advantages (simplicity, no dependencies, single file)
- Provides seamless experience across different Claude interfaces
- Opens possibility for web UI and API access

## Testing Requirements
- Concurrent read/write stress tests
- Multiple client connection scenarios
- Performance benchmarks vs single-client mode
- Data integrity verification under concurrent access

## Related Issues
- #57 (HTTP/SSE implementation) - The HTTP server could serve as the foundation for multi-client access

## Acceptance Criteria
- [ ] Multiple Claude instances can access the same memory database
- [ ] No data corruption under concurrent access
- [ ] Performance degradation < 10% vs single-client mode
- [ ] Backward compatible with existing configurations
- [ ] Clear documentation for setup and configuration