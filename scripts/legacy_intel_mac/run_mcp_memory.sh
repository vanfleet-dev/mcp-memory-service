#!/bin/bash
# run_mcp_memory.sh - Wrapper script for MCP Memory Service

# Set the base directory to the script location
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
cd "$BASE_DIR" || exit 1

# Source the virtual environment
if [ -f "$BASE_DIR/venv/bin/activate" ]; then
    source "$BASE_DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found at $BASE_DIR/venv" >&2
    echo "Please run: python -m venv venv && pip install -e ." >&2
    exit 1
fi

# Check for required packages
if ! pip show sentence-transformers >/dev/null 2>&1; then
    echo "Installing required packages..." >&2
    pip install sentence-transformers onnx onnxruntime
fi

# Set required environment variables for macOS Intel
export MCP_MEMORY_USE_ONNX=1
export MCP_MEMORY_STORAGE_BACKEND=sqlite_vec
export PYTORCH_ENABLE_MPS_FALLBACK=1

# Use default paths if not specified
if [ -z "$MCP_MEMORY_SQLITE_PATH" ]; then
    export MCP_MEMORY_SQLITE_PATH="$HOME/Library/Application Support/mcp-memory/sqlite_vec.db"
fi

if [ -z "$MCP_MEMORY_BACKUPS_PATH" ]; then
    export MCP_MEMORY_BACKUPS_PATH="$HOME/Library/Application Support/mcp-memory/backups"
fi

# Ensure directories exist with proper permissions
mkdir -p "$(dirname "$MCP_MEMORY_SQLITE_PATH")"
mkdir -p "$MCP_MEMORY_BACKUPS_PATH"
chmod -R 755 "$HOME/Library/Application Support/mcp-memory"

# Verify write permissions
touch "$HOME/Library/Application Support/mcp-memory/chroma_db/.write_test" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Cannot write to ChromaDB directory. Please check permissions." >&2
    exit 1
fi
rm -f "$HOME/Library/Application Support/mcp-memory/chroma_db/.write_test"

touch "$MCP_MEMORY_BACKUPS_PATH/.write_test" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Cannot write to backups directory. Please check permissions." >&2
    exit 1
fi
rm -f "$MCP_MEMORY_BACKUPS_PATH/.write_test"

# Log startup information
echo "Starting MCP Memory Service with:" >&2
echo "- SQLite-vec Path: $MCP_MEMORY_SQLITE_PATH" >&2
echo "- Backups Path: $MCP_MEMORY_BACKUPS_PATH" >&2
echo "- Using ONNX: Yes" >&2
echo "- Storage Backend: sqlite_vec" >&2

# Run the memory server
if command -v memory >/dev/null 2>&1; then
    # Use the installed memory command
    memory
else
    # Fallback to running the server module directly
    python -m mcp_memory_service.server
fi