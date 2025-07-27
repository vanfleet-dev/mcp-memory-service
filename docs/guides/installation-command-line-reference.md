# Installation Command Line Reference

This document provides a comprehensive reference for all command line options available in the MCP Memory Service installer (`install.py`).

## Basic Usage

```bash
python install.py [OPTIONS]
```

## Command Line Options

### Core Installation Options

#### `--dev`
Install in development mode (editable install).
```bash
python install.py --dev
```

#### `--chroma-path CHROMA_PATH`
Specify custom path for ChromaDB storage.
```bash
python install.py --chroma-path /custom/path/chromadb
```

#### `--backups-path BACKUPS_PATH`
Specify custom path for backup storage.
```bash
python install.py --backups-path /custom/path/backups
```

### Storage Backend Options

#### `--storage-backend {chromadb,sqlite_vec,auto_detect}`
Choose the storage backend:
- `chromadb`: Full-featured vector database (default for high-memory systems)
- `sqlite_vec`: Lightweight, fast alternative (default for resource-constrained systems)
- `auto_detect`: Try ChromaDB first, fallback to SQLite-vec on failure

```bash
# Force SQLite-vec backend
python install.py --storage-backend sqlite_vec

# Force ChromaDB backend  
python install.py --storage-backend chromadb

# Auto-detection with fallback
python install.py --storage-backend auto_detect
```

### Hardware-Specific Options

#### `--legacy-hardware`
Optimize installation for legacy hardware (2013-2017 Intel Macs).
- Forces SQLite-vec backend
- Enables Homebrew PyTorch integration
- Configures ONNX runtime
- Optimizes for older hardware constraints

```bash
python install.py --legacy-hardware
```

#### `--server-mode`
Install for server/headless deployment.
- Uses SQLite-vec backend for minimal dependencies
- Skips UI-related dependencies
- Optimizes for server environments

```bash
python install.py --server-mode
```

### PyTorch Configuration Options

#### `--skip-pytorch`
Skip PyTorch installation and use ONNX runtime with SQLite-vec backend.
```bash
python install.py --skip-pytorch
```

#### `--use-homebrew-pytorch`
Use existing Homebrew PyTorch installation instead of pip version.
```bash
python install.py --use-homebrew-pytorch
```

#### `--force-pytorch`
Force PyTorch installation even when using SQLite-vec (overrides auto-skip).
```bash
python install.py --force-pytorch
```

#### `--force-compatible-deps`
Force compatible versions of PyTorch and sentence-transformers for macOS Intel.
```bash
python install.py --force-compatible-deps
```

#### `--fallback-deps`
Use fallback versions for troubleshooting compatibility issues.
```bash
python install.py --fallback-deps
```

### Advanced Features

#### `--enable-http-api`
Enable HTTP/SSE API functionality for web interface.
```bash
python install.py --enable-http-api
```

#### `--migrate-from-chromadb`
Migrate existing ChromaDB installation to selected backend.
```bash
python install.py --migrate-from-chromadb --storage-backend sqlite_vec
```

### Multi-Client Setup Options

#### `--setup-multi-client` ⭐ **NEW**
Automatically configure multi-client access for any MCP-compatible applications during installation.
- Detects Claude Desktop, VS Code, Continue, Cursor, and other MCP clients
- Configures shared database access with WAL mode
- Sets up optimal environment variables
- Provides universal configuration for unknown clients

```bash
python install.py --setup-multi-client
```

#### `--skip-multi-client-prompt` ⭐ **NEW**
Skip the interactive prompt for multi-client setup.
```bash
python install.py --skip-multi-client-prompt
```

### IDE Integration Options

#### `--configure-claude-code`
Automatically configure Claude Code MCP integration with optimized settings.
```bash
python install.py --configure-claude-code
```

### Information and Help Options

#### `--help-detailed`
Show detailed hardware-specific installation recommendations.
```bash
python install.py --help-detailed
```

#### `--generate-docs`
Generate personalized setup documentation for your hardware.
```bash
python install.py --generate-docs
```

## Common Usage Patterns

### Quick Start (Recommended)
```bash
# Intelligent installer with multi-client setup
python install.py

# When prompted: "Would you like to configure multi-client access? (y/N): y"
```

### Legacy Hardware (2015 MacBook Pro, etc.)
```bash
python install.py --legacy-hardware
```

### Server Deployment
```bash
python install.py --server-mode --skip-multi-client-prompt
```

### Development Setup
```bash
python install.py --dev --setup-multi-client --enable-http-api
```

### Resource-Constrained Systems
```bash
python install.py --storage-backend sqlite_vec --skip-pytorch
```

### Migration from ChromaDB
```bash
python install.py --migrate-from-chromadb --storage-backend sqlite_vec
```

### macOS Intel Compatibility Issues
```bash
python install.py --force-compatible-deps --storage-backend sqlite_vec
```

### Multi-Client with Specific Backend
```bash
python install.py --storage-backend sqlite_vec --setup-multi-client
```

### Complete Setup with All Features
```bash
python install.py --setup-multi-client --enable-http-api --configure-claude-code
```

## Environment Variable Integration

The installer sets these environment variables based on options:

### Storage Backend Variables
```bash
# Set by --storage-backend sqlite_vec
MCP_MEMORY_STORAGE_BACKEND=sqlite_vec

# Set by --storage-backend chromadb  
MCP_MEMORY_STORAGE_BACKEND=chromadb
```

### Multi-Client Variables
```bash
# Set by --setup-multi-client
MCP_MEMORY_STORAGE_BACKEND=sqlite_vec
MCP_MEMORY_SQLITE_PRAGMAS=busy_timeout=15000,cache_size=20000
LOG_LEVEL=INFO
```

### Hardware Optimization Variables
```bash
# Set by --legacy-hardware or --use-homebrew-pytorch
MCP_MEMORY_USE_ONNX=1

# Set by GPU detection
PYTORCH_ENABLE_MPS_FALLBACK=1  # macOS Apple Silicon
MCP_MEMORY_USE_DIRECTML=1      # Windows DirectML
MCP_MEMORY_USE_ROCM=1          # Linux ROCm
```

## Installation Flow

The installer follows this sequence:

1. **System Detection** - Hardware, platform, and GPU analysis
2. **Backend Selection** - Intelligent recommendation or user choice
3. **Dependency Installation** - Platform-specific PyTorch and ML libraries
4. **Package Installation** - Core MCP Memory Service
5. **Path Configuration** - Storage directories and permissions
6. **Verification** - Installation validation and testing
7. **Multi-Client Setup** ⭐ **NEW** - Universal MCP client configuration
8. **Integration** - Claude Code and other IDE setup

## Error Handling and Fallbacks

The installer includes robust error handling:

### Storage Backend Fallbacks
```bash
# Auto-detection fallback sequence
ChromaDB → SQLite-vec → Manual intervention required
```

### PyTorch Installation Fallbacks
```bash
# Platform-specific fallback sequence
Latest PyTorch → Compatible versions → ONNX runtime → Manual installation
```

### Multi-Client Setup Fallbacks
```bash
# Multi-client setup fallback sequence
Integrated setup → Manual script → Generic instructions → Documentation
```

## Exit Codes

- `0`: Success
- `1`: Installation failure (dependencies, package installation, or path configuration)
- `2`: Verification failure (warnings only, installation may still work)

## Logging and Debugging

Enable detailed logging:
```bash
LOG_LEVEL=DEBUG python install.py --setup-multi-client
```

Generate diagnostic information:
```bash
python install.py --help-detailed
python install.py --generate-docs
```

## Platform-Specific Notes

### Windows
- Use PowerShell for environment variable persistence
- Some Unicode characters may not display correctly in older terminals
- DirectML support for GPU acceleration

### macOS
- Homebrew PyTorch integration available
- MPS acceleration for Apple Silicon
- Legacy hardware support for older Intel Macs

### Linux
- ROCm support for AMD GPUs
- CUDA support for NVIDIA GPUs
- Standard XDG directory conventions

## Integration with CI/CD

For automated deployments:
```bash
# Non-interactive installation
python install.py --server-mode --skip-multi-client-prompt --storage-backend sqlite_vec

# Docker-friendly installation
python install.py --server-mode --skip-pytorch --storage-backend sqlite_vec
```

This command line reference covers all available options for customizing your MCP Memory Service installation to meet specific requirements and environments.