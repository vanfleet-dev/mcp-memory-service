#!/bin/bash

# Kill any existing memory service processes
pkill -f "python -m mcp_memory_service.server"

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

echo "Starting MCP Memory Service for Claude..."
nohup python -m mcp_memory_service.server > /tmp/mcp_memory.log 2>&1 &

# Wait for the service to start
sleep 5

# Check if the service is running
if pgrep -f "python -m mcp_memory_service.server" > /dev/null; then
    echo "✅ Memory service started successfully!"
    echo "Now restart Claude to use the memory service."
    echo "Log file: /tmp/mcp_memory.log"
else
    echo "❌ Memory service failed to start."
    echo "Check the log file for errors: /tmp/mcp_memory.log"
    cat /tmp/mcp_memory.log
fi