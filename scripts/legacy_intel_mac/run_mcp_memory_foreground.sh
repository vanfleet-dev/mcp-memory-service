#!/bin/bash

# Set the base directory to the script location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$BASE_DIR" || exit 1

# Activate the Python 3.10 virtual environment
source "$BASE_DIR/venv_py310/bin/activate"

# Set required environment variables
export MCP_MEMORY_USE_ONNX=1
export MCP_MEMORY_STORAGE_BACKEND=sqlite_vec
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Create required directories
echo "Creating required directories..."
mkdir -p "$HOME/Library/Application Support/mcp-memory/chroma_db"
mkdir -p "$HOME/Library/Application Support/mcp-memory/backups"
mkdir -p "$HOME/Library/Application Support/mcp-memory/sqlite_vec.db"
chmod -R 755 "$HOME/Library/Application Support/mcp-memory"

# Verify write permissions
touch "$HOME/Library/Application Support/mcp-memory/chroma_db/.write_test" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Cannot write to ChromaDB directory. Please check permissions." >&2
    exit 1
fi
rm -f "$HOME/Library/Application Support/mcp-memory/chroma_db/.write_test"

touch "$HOME/Library/Application Support/mcp-memory/backups/.write_test" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Cannot write to backups directory. Please check permissions." >&2
    exit 1
fi
rm -f "$HOME/Library/Application Support/mcp-memory/backups/.write_test"

echo "Starting MCP Memory Service in foreground mode..."
echo "Press Ctrl+C to stop the service."
python -m mcp_memory_service.server