# Legacy Intel Mac Support Scripts

These scripts are specifically designed to support MCP Memory Service on older Intel-based Mac hardware. They address various compatibility issues that can arise with PyTorch, NumPy, and other dependencies on these systems.

## Why These Scripts Are Needed

Intel-based Mac systems, especially older models, face specific challenges:

1. **PyTorch Compatibility**: PyTorch has shifted focus to Apple Silicon, creating compatibility gaps for Intel Macs
2. **Python Version Sensitivity**: Python 3.13+ introduces breaking changes affecting ML libraries
3. **NumPy Version Conflicts**: Newer NumPy 2.x conflicts with older ML libraries
4. **Dependency Resolution**: Specific package versions are needed for compatibility

## Available Scripts

### 1. `claude_memory.sh`

A foreground script that:
- Runs the memory service with Python 3.10
- Sets all required environment variables
- Shows live output for debugging
- Can be stopped with Ctrl+C

Usage:
```bash
./scripts/legacy_intel_mac/claude_memory.sh
```

### 2. `start_memory_for_claude.sh`

A background script that:
- Starts the memory service as a background process
- Verifies the service is running
- Provides helpful error reporting
- Allows closing the terminal window

Usage:
```bash
./scripts/legacy_intel_mac/start_memory_for_claude.sh
```

### 3. `run_mcp_memory_foreground.sh`

A simplified script that:
- Focuses solely on running the service
- Minimal setup for debugging
- Useful for understanding the core requirements

Usage:
```bash
./scripts/legacy_intel_mac/run_mcp_memory_foreground.sh
```

## Requirements

These scripts assume:
- Python 3.10 is installed
- A virtual environment called `venv_py310` in the project root
- Required dependencies have been installed following the [Intel Mac Setup Guide](../../docs/platforms/macos-intel.md)

## Related Documentation

For comprehensive setup instructions, please refer to:
- [Intel Mac Setup Guide](../../docs/platforms/macos-intel.md) - Detailed setup instructions
- [Hardware Compatibility](../../docs/DOCUMENTATION_AUDIT.md) - Platform compatibility matrix