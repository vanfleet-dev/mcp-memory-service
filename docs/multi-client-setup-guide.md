# Multi-Client Setup Guide

This guide covers manual multi-client setup for the MCP Memory Service. **For most users, we recommend using the [new integrated setup](guides/universal-multi-client-setup.md)** which is built into the main installer.

## New: Integrated Setup (Recommended)

🚀 **The easiest way to set up multi-client access is now during installation:**

```bash
python install.py
# When prompted: "Would you like to configure multi-client access? (y/N): y"
```

**Benefits of integrated setup:**
- ✅ Automatic detection of Claude Desktop, VS Code, Continue, Cursor, and other MCP clients
- ✅ Universal compatibility beyond just Claude applications  
- ✅ Zero manual configuration required
- ✅ Future-proof setup for any MCP application

**See the [Universal Multi-Client Setup Guide](guides/universal-multi-client-setup.md) for complete details.**

---

## Manual Setup (Legacy)

The information below covers manual setup for advanced users or troubleshooting scenarios.

### Overview

The MCP Memory Service supports multi-client access through two phases:
- **Phase 1: WAL Mode** - Direct SQLite access with Write-Ahead Logging (recommended)
- **Phase 2: HTTP Coordination** - Intelligent HTTP server coordination (advanced)

This guide focuses on **Phase 1 (WAL Mode)** which provides reliable concurrent access without complexity.

## Quick Setup

### 1. Run the Setup Script

```bash
python setup_multi_client_complete.py
```

This script will:
- Test your system for multi-client compatibility
- Configure optimal environment variables
- Verify WAL mode functionality
- Provide Claude Desktop configuration

### 2. Update Claude Desktop Configuration

Add the following to your Claude Desktop config (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "C:\\REPOSITORIES\\mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PRAGMAS": "busy_timeout=15000,cache_size=20000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### 3. Set Environment Variables (Permanent)

Run these commands in PowerShell as Administrator:

```powershell
[System.Environment]::SetEnvironmentVariable("MCP_MEMORY_STORAGE_BACKEND", "sqlite_vec", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("MCP_MEMORY_SQLITE_PRAGMAS", "busy_timeout=15000,cache_size=20000", [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable("LOG_LEVEL", "INFO", [System.EnvironmentVariableTarget]::User)
```

Or use `setx` commands:

```cmd
setx MCP_MEMORY_STORAGE_BACKEND "sqlite_vec"
setx MCP_MEMORY_SQLITE_PRAGMAS "busy_timeout=15000,cache_size=20000"  
setx LOG_LEVEL "INFO"
```

### 4. Restart Applications

- Close Claude Desktop completely (check system tray)
- Close any Claude Code sessions
- Restart both applications

## Testing Multi-Client Access

### Basic Test

1. **In Claude Desktop**: "Remember: I'm testing from Claude Desktop"
2. **In Claude Code**: "What did I ask you to remember?"
3. **Expected**: Both should access the same memory database

### Advanced Test

Run the verification script:

```bash
python test_multi_client_verification.py
```

## How It Works

### WAL Mode Features

- **Multiple Readers**: Several clients can read simultaneously
- **Single Writer**: One client writes at a time (queued automatically)
- **Automatic Retry**: 15-second timeout with exponential backoff
- **Performance Cache**: 20MB cache for faster access
- **No Lock Conflicts**: WAL mode prevents most database locking issues

### Architecture

```
Claude Desktop ←→ SQLite-vec Database (WAL Mode) ←→ Claude Code
                            ↓
                   Shared Memory Storage
                   • memories.db
                   • memories.db-wal
                   • memories.db-shm
```

## Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_MEMORY_STORAGE_BACKEND` | `chroma` | Set to `sqlite_vec` for multi-client |
| `MCP_MEMORY_SQLITE_PRAGMAS` | - | SQLite optimization settings |
| `MCP_MEMORY_SQLITE_PATH` | auto | Custom database location |
| `LOG_LEVEL` | `WARNING` | Set to `INFO` for coordination logs |

### SQLite Pragma Options

The `MCP_MEMORY_SQLITE_PRAGMAS` variable accepts comma-separated key=value pairs:

```bash
# Performance optimized
MCP_MEMORY_SQLITE_PRAGMAS="busy_timeout=15000,cache_size=20000,temp_store=MEMORY"

# High concurrency
MCP_MEMORY_SQLITE_PRAGMAS="busy_timeout=30000,wal_autocheckpoint=1000"

# Conservative/safe mode  
MCP_MEMORY_SQLITE_PRAGMAS="synchronous=FULL,busy_timeout=60000"
```

## Troubleshooting

### Common Issues

#### 1. Database Lock Errors
```
sqlite3.OperationalError: database is locked
```

**Solutions:**
- Ensure WAL mode is enabled (check logs for "WAL mode enabled")
- Increase busy timeout: `MCP_MEMORY_SQLITE_PRAGMAS="busy_timeout=30000"`
- Restart both applications completely

#### 2. Environment Variables Not Applied
```
[WARNING] Backend is 'None', should be 'sqlite_vec'
```

**Solutions:**
- Run setup script again: `python setup_multi_client_complete.py`
- Manually set variables using `setx` commands above
- Restart applications after setting variables

#### 3. Configuration Not Found
```
Storage backend not configured
```

**Solutions:**
- Verify Claude Desktop config file exists
- Check config syntax is valid JSON
- Ensure file path in config is correct

### Debug Mode

Enable detailed logging:

```bash
set LOG_LEVEL=DEBUG
# Then restart applications
```

Look for these log messages:
- "SQLite pragmas applied: ..."
- "WAL mode enabled for concurrent access" 
- "Detected coordination mode: direct"

## Advanced Configuration

### Enable HTTP Coordination (Phase 2)

For advanced users who want HTTP server coordination:

```json
{
  "env": {
    "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
    "MCP_MEMORY_HTTP_AUTO_START": "true",
    "MCP_HTTP_PORT": "8000"
  }
}
```

This enables automatic HTTP server detection and coordination.

### Custom Database Location

```json
{
  "env": {
    "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
    "MCP_MEMORY_SQLITE_PATH": "C:\\MyCustomPath\\memory.db"
  }
}
```

### Performance Tuning

For systems with many concurrent operations:

```bash
MCP_MEMORY_SQLITE_PRAGMAS="busy_timeout=30000,cache_size=50000,mmap_size=268435456"
```

## Verification Commands

### Check Configuration
```bash
python -c "import os; print('Backend:', os.getenv('MCP_MEMORY_STORAGE_BACKEND')); print('Pragmas:', os.getenv('MCP_MEMORY_SQLITE_PRAGMAS'))"
```

### Test Storage Initialization
```bash
python test_multi_client_verification.py
```

### Check WAL Files
```bash
dir %LOCALAPPDATA%\mcp-memory\*.db*
```

Should show:
- `sqlite_vec.db` (main database)
- `sqlite_vec.db-wal` (WAL file)
- `sqlite_vec.db-shm` (shared memory)

## Success Criteria

✅ **Setup Complete When:**
- Both Claude Desktop and Claude Code start without errors
- WAL mode messages appear in logs
- Memories stored in one client appear in the other
- No "database is locked" errors occur
- WAL files (.db-wal, .db-shm) are created

## Next Steps

Once multi-client access is working:

1. **Regular Usage**: Use both clients normally - coordination is automatic
2. **Monitor Performance**: Check logs occasionally for any issues
3. **Backup Strategy**: WAL mode creates additional files to backup
4. **Scaling Up**: For 3+ clients, consider enabling HTTP coordination

## Support

For issues not covered in this guide:

1. Check [troubleshooting section](docs/sqlite-vec-backend.md#troubleshooting) in main docs
2. Run diagnostic script: `python test_multi_client_verification.py`
3. Enable debug logging: `set LOG_LEVEL=DEBUG`
4. Review logs for specific error messages

The multi-client setup is designed to be robust and self-healing. Most issues resolve with application restarts after proper configuration.