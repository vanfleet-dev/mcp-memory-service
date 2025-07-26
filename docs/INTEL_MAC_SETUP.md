# Intel Mac Setup Guide for MCP Memory Service

This guide addresses the specific challenges of running the MCP Memory Service on Intel-based Mac hardware.

## Why a Special Setup is Needed

Intel-based Mac systems require special consideration for several reasons:

1. **PyTorch Compatibility**: PyTorch has moved toward optimizing for Apple Silicon, with some compatibility challenges on Intel Macs.
2. **NumPy Version Conflicts**: Newer NumPy 2.x can cause compatibility issues with other ML libraries.
3. **Python Version Sensitivity**: Python 3.13+ has introduced breaking changes that affect ML libraries.
4. **Sentence Transformers Dependencies**: The embedding models require specific versions of dependencies.

## Setup Instructions

### Prerequisites

- Python 3.10 (recommended) installed on your system
- Git to clone the repository
- Ability to run shell scripts

### Installation Steps

1. **Clone the repository** (if not already done):
   ```bash
   git clone https://github.com/yourusername/mcp-memory-service.git
   cd mcp-memory-service
   ```

2. **Create a Python 3.10 virtual environment**:
   ```bash
   python3.10 -m venv venv_py310
   source venv_py310/bin/activate
   ```

3. **Install the package and dependencies**:
   ```bash
   pip install -e .
   pip install sentence-transformers onnx onnxruntime
   ```

4. **Downgrade NumPy** to ensure compatibility:
   ```bash
   pip uninstall -y numpy
   pip install numpy==1.25.2
   ```

5. **Use one of the provided scripts** to start the memory service:
   ```bash
   # For foreground mode (shows all output, can be stopped with Ctrl+C)
   ./scripts/legacy_intel_mac/claude_memory.sh
   
   # For background mode (can close terminal after starting)
   ./scripts/legacy_intel_mac/start_memory_for_claude.sh
   ```

## Troubleshooting

If you encounter issues:

1. **Dependency Conflicts**: If you see errors about incompatible dependencies, try:
   ```bash
   pip uninstall -y tokenizers
   pip install tokenizers==0.21.0
   ```

2. **ChromaDB Errors**: Ensure storage directories exist and have proper permissions:
   ```bash
   mkdir -p "$HOME/Library/Application Support/mcp-memory/chroma_db"
   mkdir -p "$HOME/Library/Application Support/mcp-memory/backups"
   chmod -R 755 "$HOME/Library/Application Support/mcp-memory"
   ```

3. **Sentence Transformers Not Available**: This warning is normal on first run, but should resolve after installation.

## Environment Variables

These environment variables help optimize the service for Intel Macs:

- `MCP_MEMORY_USE_ONNX=1`: Use ONNX runtime for better performance on Intel
- `MCP_MEMORY_STORAGE_BACKEND=sqlite_vec`: Use SQLite vector store backend 
- `PYTORCH_ENABLE_MPS_FALLBACK=1`: Enable CPU fallback for PyTorch operations

## Why This Approach

While this setup is more involved than on Apple Silicon Macs, it addresses several hardware-specific issues:

1. **Memory Efficiency**: Using ONNX runtime reduces memory consumption
2. **Stability**: Specific package versions ensure stable operation
3. **Compatibility**: Python 3.10 provides the best compatibility with ML libraries

The shell script provides a convenient way to set all required environment variables and start the service with the correct configuration.

## Alternative Approaches

If this approach doesn't work for you, consider:

1. Using Docker to isolate the environment (may be slower)
2. Running the service on a different machine and connecting remotely
3. Using a simpler storage backend with `MCP_MEMORY_STORAGE_BACKEND=simple` (fewer features)