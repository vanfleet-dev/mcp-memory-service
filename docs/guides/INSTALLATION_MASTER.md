# MCP Memory Service - Complete Installation Guide

**Version**: 0.2.2+  
**Last Updated**: 2025-07-26  
**Supports**: ChromaDB + SQLite-vec backends, HTTP/SSE API

## Quick Installation by Hardware Type

### 🖥️ Legacy Hardware (2013-2017 Intel Macs)
**Best for**: 2015 MacBook Pro, older Intel Macs without GPU

```bash
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service
python install.py --legacy-hardware
```

**What this does:**
- ✅ Detects older Intel Mac hardware
- ✅ Recommends SQLite-vec backend (lightweight)
- ✅ Uses Homebrew PyTorch if available (better compatibility)
- ✅ Configures ONNX runtime for CPU-only inference
- ✅ Optimizes for limited memory systems

### 🚀 Modern Hardware (2018+ Macs, GPU-enabled systems)
**Best for**: M1/M2/M3 Macs, modern Intel systems, Windows with GPU

```bash
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service
python install.py
```

**What this does:**
- ✅ Auto-detects available hardware acceleration
- ✅ Recommends ChromaDB for full features
- ✅ Configures GPU acceleration (CUDA/MPS/DirectML)
- ✅ Installs latest PyTorch and sentence-transformers

### 🌐 Server/Headless Installation
**Best for**: Linux servers, Docker deployments, CI/CD

```bash
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service
python install.py --server-mode --storage-backend sqlite_vec
```

## Installation Methods

### Method 1: Intelligent Installer (Recommended)

The new unified installer automatically detects your hardware and recommends the optimal configuration:

```bash
# Clone repository
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run intelligent installer
python install.py
```

**Installer Features:**
- 🧠 **Hardware Detection**: Automatically detects CPU, GPU, memory, and platform
- 🎯 **Smart Recommendations**: Suggests optimal backend and configuration
- 🔧 **Platform Optimization**: Handles macOS Intel issues, Windows CUDA, Linux variations
- 📦 **Dependency Management**: Installs compatible PyTorch and ML library versions
- ⚙️ **Auto-Configuration**: Generates Claude Desktop config and environment variables

### Method 2: Manual Backend Selection

If you want to explicitly choose your storage backend:

```bash
# Choose SQLite-vec (lightweight, fast)
python install.py --storage-backend sqlite_vec

# Choose ChromaDB (full-featured)
python install.py --storage-backend chromadb

# Auto-detect (try ChromaDB, fallback to SQLite-vec)
python install.py --storage-backend auto_detect
```

### Method 3: Docker Installation

For consistent cross-platform deployment:

```bash
# Pull latest image
docker pull doobidoo/mcp-memory-service:latest

# Run with SQLite-vec backend
docker run -d -p 8000:8000 \
  -e MCP_MEMORY_STORAGE_BACKEND=sqlite_vec \
  -v $(pwd)/data:/app/data \
  doobidoo/mcp-memory-service:latest
```

## Storage Backend Selection Guide

### SQLite-vec Backend 🪶
**Recommended for**: Legacy hardware, low-memory systems, simple deployments

**Pros:**
- ✅ Single file database (easy backup/sharing)
- ✅ 10x faster startup than ChromaDB
- ✅ Lower memory usage (< 100MB)
- ✅ No external dependencies
- ✅ Works well with ONNX runtime
- ✅ Supports HTTP/SSE API

**Best for:**
- 2015 MacBook Pro and similar older hardware
- Systems with < 4GB RAM
- Docker/serverless deployments
- Quick prototyping and testing

### ChromaDB Backend 📦
**Recommended for**: Modern hardware, feature-rich deployments

**Pros:**
- ✅ Advanced vector search features
- ✅ Rich metadata support
- ✅ Extensive ecosystem integration
- ✅ Battle-tested at scale
- ✅ Advanced filtering capabilities

**Best for:**
- Modern Macs (M1/M2/M3)
- Systems with > 8GB RAM
- GPU-enabled systems
- Production deployments requiring advanced features

## Hardware-Specific Installation

### macOS Intel (2013-2017) - Legacy Hardware Path

**Problem**: Older Intel Macs often struggle with ChromaDB installation and modern PyTorch versions.

**Solution**: Optimized legacy hardware installation

```bash
# Step 1: Check if you have Homebrew PyTorch
brew list pytorch || echo "Consider: brew install pytorch"

# Step 2: Use legacy hardware installation
python install.py --legacy-hardware

# Step 3: Verify installation
python scripts/verify_environment.py
```

**What happens:**
1. **Hardware Detection**: Identifies macOS Intel system
2. **Backend Selection**: Automatically selects SQLite-vec
3. **PyTorch Handling**: Uses Homebrew PyTorch if available
4. **Fallback Configuration**: Sets up ONNX runtime for compatibility
5. **Memory Optimization**: Configures for limited resources

**Environment Variables Set:**
```bash
export MCP_MEMORY_STORAGE_BACKEND=sqlite_vec
export MCP_MEMORY_USE_ONNX=1
export MCP_MEMORY_SQLITE_PATH="$HOME/Library/Application Support/mcp-memory/sqlite_vec.db"
```

### macOS Apple Silicon (M1/M2/M3)

```bash
# Standard installation works great
python install.py

# Uses MPS acceleration automatically
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

### Windows with GPU

```bash
# Automatic CUDA detection and installation
python install.py

# Or use Windows-specific installer
python scripts/install_windows.py
```

### Windows CPU-only

```bash
# Optimized for CPU-only systems
python install.py --storage-backend sqlite_vec
```

### Linux Server

```bash
# Headless installation
python install.py --server-mode --storage-backend sqlite_vec
```

## Verification and Testing

After installation, verify everything works:

```bash
# Check environment
python scripts/verify_environment.py

# Test memory operations
python -c "
from mcp_memory_service.storage import get_storage
storage = get_storage()
print('✅ Storage backend initialized successfully')
"

# Test with sample memory
python scripts/test_memory_simple.py
```

## Claude Desktop Integration

The installer automatically generates Claude Desktop configuration. Here's what it creates:

### For SQLite-vec Backend
```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PATH": "/path/to/sqlite_vec.db",
        "MCP_MEMORY_USE_ONNX": "1"
      }
    }
  }
}
```

### For ChromaDB Backend
```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-memory-service", "run", "memory"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "chromadb",
        "MCP_MEMORY_CHROMA_PATH": "/path/to/chroma_db"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'sentence_transformers'`
**Solution**: 
```bash
# For legacy hardware
python install.py --legacy-hardware

# For modern systems
pip install sentence-transformers>=2.2.2
```

**Issue**: ChromaDB installation fails on older macOS Intel
**Solution**: 
```bash
python install.py --storage-backend sqlite_vec --use-homebrew-pytorch
```

**Issue**: `CUDA out of memory` errors
**Solution**: 
```bash
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
export MCP_MEMORY_USE_ONNX=1
```

### Platform-Specific Troubleshooting

- **macOS Intel Legacy**: See [docs/platforms/macos-intel-legacy.md](../platforms/macos-intel-legacy.md)
- **Windows**: See [docs/platforms/windows.md](../platforms/windows.md)
- **Linux**: See [docs/platforms/linux.md](../platforms/linux.md)

## Migration from Existing Installation

If you're upgrading from a ChromaDB-only installation:

```bash
# Run migration script
python scripts/migrate_chroma_to_sqlite.py

# Or use installer migration mode
python install.py --migrate-from-chromadb
```

## HTTP/SSE API Installation

To enable the new HTTP/SSE interface:

```bash
# Install with HTTP support
python install.py --enable-http-api

# Run HTTP server
python scripts/run_http_server.py
```

Access the web interface at: http://localhost:8000

## Next Steps

After successful installation:

1. **Test the installation**: Run `python scripts/test_memory_simple.py`
2. **Configure Claude Desktop**: Use the generated config file
3. **Read the user guide**: See [docs/guides/usage.md](usage.md)
4. **Explore HTTP API**: See [docs/api/HTTP_SSE_API.md](../api/HTTP_SSE_API.md)
5. **Join the community**: Report issues and get help on GitHub

## Installation Command Reference

```bash
# Basic installation
python install.py

# Legacy hardware (2015 MacBook Pro scenario)
python install.py --legacy-hardware

# Specific backend selection
python install.py --storage-backend {chromadb|sqlite_vec|auto_detect}

# Development installation
python install.py --dev

# Server mode (headless)
python install.py --server-mode

# With HTTP/SSE API
python install.py --enable-http-api

# Migration mode
python install.py --migrate-from-chromadb

# Get detailed help
python install.py --help-detailed
```