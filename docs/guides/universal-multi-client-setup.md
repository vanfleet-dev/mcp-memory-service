# Universal Multi-Client Setup Guide

This guide covers the new integrated multi-client setup functionality in the MCP Memory Service, which enables seamless memory sharing across any MCP-compatible applications during the installation process.

## Overview

As of the latest version, multi-client setup is **integrated directly into the main installation process**. The installer automatically detects MCP-compatible applications and offers to configure universal memory sharing during installation.

### What's New

- ✅ **Integrated Setup**: Multi-client configuration is now part of `python install.py`
- ✅ **Universal Compatibility**: Supports any MCP client (Claude, VS Code, Continue, Cursor, etc.)
- ✅ **Automatic Detection**: Finds and configures all installed MCP applications
- ✅ **Intelligent Prompting**: Only offers when appropriate (SQLite-vec backend)
- ✅ **Zero Manual Configuration**: Automatically updates client configuration files

## Quick Start

### During Installation (Recommended)

```bash
# Run the installer - you'll be prompted for multi-client setup
python install.py

# When you see this prompt, choose 'y':
# 🌐 Multi-Client Access Available!
# Would you like to configure multi-client access? (y/N): y
```

### Command Line Options

```bash
# Automatic multi-client setup (no prompts)
python install.py --setup-multi-client

# Skip the multi-client prompt entirely
python install.py --skip-multi-client-prompt

# Combined with other options
python install.py --storage-backend sqlite_vec --setup-multi-client
```

## Supported Applications

The integrated setup automatically detects and configures:

### Automatically Configured
- **Claude Desktop**: Updates `claude_desktop_config.json` with multi-client settings
- **Continue IDE**: Modifies Continue configuration files
- **Generic MCP Clients**: Updates `.mcp.json` and similar configuration files

### Guided Configuration
- **VS Code with MCP Extension**: Provides specific setup instructions
- **Cursor IDE**: MCP extension configuration guidance
- **Claude Code**: Project-level `.mcp.json` configuration instructions

### Future Applications
- **Any MCP Client**: Generic configuration provided for unknown applications

## How It Works

### 1. Detection Phase
The installer scans for:
```
Claude Desktop:
  - Windows: %APPDATA%\Claude\claude_desktop_config.json
  - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
  - Linux: ~/.config/Claude/claude_desktop_config.json

VS Code/Cursor:
  - Windows: %APPDATA%\Code\User\settings.json
  - macOS: ~/Library/Application Support/Code/User/settings.json
  - Linux: ~/.config/Code/User/settings.json

Continue IDE:
  - ~/.continue/config.json
  - ~/.config/continue/config.json
  - %APPDATA%\continue\config.json

Generic MCP:
  - ~/.mcp.json
  - ~/.config/mcp/config.json
  - ./.mcp.json (project level)
```

### 2. Configuration Phase
For each detected client:
- **Automatic**: Direct configuration file updates
- **Guided**: Step-by-step instructions displayed
- **Generic**: Universal configuration templates provided

### 3. Validation Phase
- Tests WAL mode coordination
- Verifies shared database access
- Confirms environment variable setup

## Configuration Details

### Automatic Configuration

**Claude Desktop Example:**
```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PRAGMAS": "busy_timeout=15000,cache_size=20000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Continue IDE Example:**
```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PRAGMAS": "busy_timeout=15000,cache_size=20000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Environment Variables

The setup configures these environment variables:

```bash
# Storage backend (required for multi-client)
MCP_MEMORY_STORAGE_BACKEND=sqlite_vec

# SQLite optimization for concurrent access
MCP_MEMORY_SQLITE_PRAGMAS=busy_timeout=15000,cache_size=20000

# Logging level for coordination debugging
LOG_LEVEL=INFO
```

### Manual Configuration Template

For applications not automatically detected:

```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PRAGMAS": "busy_timeout=15000,cache_size=20000",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Technical Implementation

### WAL Mode Coordination

The setup uses SQLite Write-Ahead Logging (WAL) mode for safe concurrent access:

```sql
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=15000;
PRAGMA cache_size=20000;
PRAGMA synchronous=NORMAL;
```

### Shared Database Location

All clients access the same database:
- **Windows**: `%LOCALAPPDATA%\mcp-memory\sqlite_vec.db`
- **macOS**: `~/Library/Application Support/mcp-memory/sqlite_vec.db`
- **Linux**: `~/.local/share/mcp-memory/sqlite_vec.db`

### Connection Retry Logic

Built-in retry mechanism handles transient locks:
- 15-second timeout for database operations
- Exponential backoff for failed connections
- Graceful fallback to single-client mode if needed

## Integration Flow

### 1. Prerequisites Check
```python
def should_offer_multi_client_setup(args, final_backend):
    # Only offer if using SQLite-vec backend
    if final_backend != "sqlite_vec":
        return False
    
    # Don't offer in server mode
    if args.server_mode:
        return False
    
    # Skip if explicitly disabled
    if args.skip_multi_client_prompt:
        return False
    
    return True
```

### 2. Client Detection
```python
def detect_mcp_clients():
    clients = {}
    
    # Check Claude Desktop
    # Check VS Code/Cursor  
    # Check Continue IDE
    # Check generic MCP configs
    
    return clients
```

### 3. Configuration Application
```python
def configure_detected_clients(clients, system_info):
    success_count = 0
    
    for client_type, config_path in clients.items():
        if client_type == 'claude_desktop':
            success_count += configure_claude_desktop_multi_client(config_path)
        elif client_type == 'continue':
            success_count += configure_continue_multi_client(config_path)
        # ... other clients
    
    return success_count
```

## Benefits

### For Users
1. **One-Step Setup**: Multi-client access configured during installation
2. **Universal Compatibility**: Works with any MCP application
3. **Automatic Discovery**: Finds and configures all installed clients
4. **Future-Proof**: Generic configuration for upcoming MCP applications

### For Developers  
1. **Shared Context**: Memory persists across development tools
2. **Seamless Workflow**: Switch between IDEs without losing context
3. **Consistent State**: Single source of truth for project memories
4. **Tool Integration**: Works with existing development environments

## Troubleshooting

### Setup Issues

**Problem**: Multi-client prompt not appearing
```bash
# Check if SQLite-vec backend is selected
echo $MCP_MEMORY_STORAGE_BACKEND

# Should output: sqlite_vec
# If not, reinstall with: python install.py --storage-backend sqlite_vec
```

**Problem**: Client not detected
```bash
# Manually run detection
python -c "
from install import detect_mcp_clients, print_detected_clients
clients = detect_mcp_clients()
print_detected_clients(clients)
"
```

**Problem**: Configuration failed
```bash
# Use manual setup script
python setup_multi_client_complete.py
```

### Runtime Issues

**Problem**: Database locks
```bash
# Check WAL mode files exist
ls ~/.local/share/mcp-memory/sqlite_vec.db*

# Should show:
# sqlite_vec.db      (main database)
# sqlite_vec.db-wal  (WAL file)
# sqlite_vec.db-shm  (shared memory)
```

**Problem**: Environment variables not set
```bash
# Check current environment
env | grep MCP_MEMORY

# Set manually if needed
export MCP_MEMORY_STORAGE_BACKEND=sqlite_vec
export MCP_MEMORY_SQLITE_PRAGMAS="busy_timeout=15000,cache_size=20000"
```

## Migration from Manual Setup

If you previously used the manual `setup_multi_client_complete.py` script:

1. **Backup current configuration**:
   ```bash
   cp ~/.mcp.json ~/.mcp.json.backup
   cp "%APPDATA%\Claude\claude_desktop_config.json" claude_config_backup.json
   ```

2. **Run integrated setup**:
   ```bash
   python install.py --setup-multi-client
   ```

3. **Verify all clients work**:
   - Test memory storage in one application
   - Verify retrieval in another application
   - Check that WAL files are created

## Advanced Configuration

### Custom Database Location

```json
{
  "env": {
    "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
    "MCP_MEMORY_SQLITE_PATH": "/custom/path/memory.db",
    "MCP_MEMORY_SQLITE_PRAGMAS": "busy_timeout=30000,cache_size=50000"
  }
}
```

### Performance Tuning

For systems with many concurrent clients:

```bash
export MCP_MEMORY_SQLITE_PRAGMAS="busy_timeout=30000,cache_size=50000,mmap_size=268435456"
```

### HTTP Coordination (Advanced)

For 3+ clients or complex scenarios:

```json
{
  "env": {
    "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
    "MCP_MEMORY_HTTP_AUTO_START": "true",
    "MCP_HTTP_PORT": "8000"
  }
}
```

## Future Enhancements

The integrated multi-client setup framework supports:

1. **New MCP Applications**: Automatic detection patterns for future clients
2. **Enhanced Coordination**: HTTP-based coordination for complex scenarios
3. **Cloud Synchronization**: Multi-device memory sharing capabilities
4. **Conflict Resolution**: Advanced merge strategies for concurrent edits

## Support

For issues with the integrated multi-client setup:

1. **Check logs**: Enable debug logging with `LOG_LEVEL=DEBUG`
2. **Manual setup**: Use `python setup_multi_client_complete.py` as fallback
3. **Documentation**: See [Multi-Client Setup Guide](multi-client-setup-guide.md) for detailed manual instructions
4. **Issue reporting**: Include client detection output and error logs

The integrated multi-client setup represents a major advancement in making the MCP Memory Service truly universal across development environments.