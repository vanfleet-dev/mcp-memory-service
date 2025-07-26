#!/bin/bash

# This script runs the MCP Memory Service in foreground mode for Claude
# Press Ctrl+C to stop the service

# Set the base directory to the script location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$BASE_DIR" || exit 1

# Activate the Python 3.10 virtual environment
source "$BASE_DIR/venv_py310/bin/activate"

# Set required environment variables
export MCP_MEMORY_USE_ONNX=1
export MCP_MEMORY_STORAGE_BACKEND=sqlite_vec
export PYTORCH_ENABLE_MPS_FALLBACK=1
export MCP_MEMORY_DEBUG=1
export PYTHONUNBUFFERED=1

# Create required directories
echo "Creating required directories..."
mkdir -p "$HOME/Library/Application Support/mcp-memory/chroma_db"
mkdir -p "$HOME/Library/Application Support/mcp-memory/backups"
mkdir -p "$HOME/Library/Application Support/mcp-memory/sqlite_vec.db"
chmod -R 755 "$HOME/Library/Application Support/mcp-memory"

echo "Starting MCP Memory Service for Claude..."
echo "Press Ctrl+C to stop the service."
echo "======================================"
python -m mcp_memory_service.server