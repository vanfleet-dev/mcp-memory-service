# MCP Memory Service

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub stars](https://img.shields.io/github/stars/doobidoo/mcp-memory-service?style=social)](https://github.com/doobidoo/mcp-memory-service/stargazers)
[![Production Ready](https://img.shields.io/badge/Production-Ready-brightgreen?style=flat&logo=checkmark)](https://github.com/doobidoo/mcp-memory-service#-in-production)

[![Works with Claude](https://img.shields.io/badge/Works%20with-Claude-blue)](https://claude.ai)
[![Works with Cursor](https://img.shields.io/badge/Works%20with-Cursor-orange)](https://cursor.sh)
[![MCP Protocol](https://img.shields.io/badge/MCP-Compatible-4CAF50?style=flat)](https://modelcontextprotocol.io/)
[![Multi-Client](https://img.shields.io/badge/Multi--Client-13+%20Apps-FF6B35?style=flat)](https://github.com/doobidoo/mcp-memory-service/wiki)

**Universal MCP memory service** providing **semantic memory search** and persistent storage for **AI assistants**. Works with **Claude Desktop, VS Code, Cursor, Continue, and 13+ AI applications** with **SQLite-vec** for fast local search and **Cloudflare** for global distribution.

<img width="240" alt="MCP Memory Service" src="https://github.com/user-attachments/assets/eab1f341-ca54-445c-905e-273cd9e89555" />

## 🚀 Quick Start (2 minutes)

### Universal Installer (Recommended)
```bash
# Clone and install with automatic platform detection
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service
python install.py
```

### Docker (Fastest)
```bash
# For MCP protocol (Claude Desktop)
docker-compose up -d

# For HTTP API (Web Dashboard)
docker-compose -f docker-compose.http.yml up -d
```

### Smithery (Claude Desktop)
```bash
# Auto-install for Claude Desktop
npx -y @smithery/cli install @doobidoo/mcp-memory-service --client claude
```

## ⚠️ First-Time Setup Expectations

On your first run, you'll see some warnings that are **completely normal**:

- **"WARNING: Failed to load from cache: No snapshots directory"** - The service is checking for cached models (first-time setup)
- **"WARNING: Using TRANSFORMERS_CACHE is deprecated"** - Informational warning, doesn't affect functionality
- **Model download in progress** - The service automatically downloads a ~25MB embedding model (takes 1-2 minutes)

These warnings disappear after the first successful run. The service is working correctly! For details, see our [First-Time Setup Guide](docs/first-time-setup.md).

## 📚 Complete Documentation

**👉 Visit our comprehensive [Wiki](https://github.com/doobidoo/mcp-memory-service/wiki) for detailed guides:**

### 🚀 Setup & Installation
- **[📋 Installation Guide](https://github.com/doobidoo/mcp-memory-service/wiki/01-Installation-Guide)** - Complete installation for all platforms and use cases
- **[🖥️ Platform Setup Guide](https://github.com/doobidoo/mcp-memory-service/wiki/02-Platform-Setup-Guide)** - Windows, macOS, and Linux optimizations  
- **[🔗 Integration Guide](https://github.com/doobidoo/mcp-memory-service/wiki/03-Integration-Guide)** - Claude Desktop, Claude Code, VS Code, and more

### 🧠 Advanced Topics
- **[🧠 Advanced Configuration](https://github.com/doobidoo/mcp-memory-service/wiki/04-Advanced-Configuration)** - Integration patterns, best practices, workflows
- **[⚡ Performance Optimization](https://github.com/doobidoo/mcp-memory-service/wiki/05-Performance-Optimization)** - Speed up queries, optimize resources, scaling
- **[👨‍💻 Development Reference](https://github.com/doobidoo/mcp-memory-service/wiki/06-Development-Reference)** - Claude Code hooks, API reference, debugging

### 🔧 Help & Reference
- **[🔧 Troubleshooting Guide](https://github.com/doobidoo/mcp-memory-service/wiki/07-TROUBLESHOOTING)** - Solutions for common issues
- **[❓ FAQ](https://github.com/doobidoo/mcp-memory-service/wiki/08-FAQ)** - Frequently asked questions
- **[📝 Examples](https://github.com/doobidoo/mcp-memory-service/wiki/09-Examples)** - Practical code examples and workflows

## ✨ Key Features

### 🧠 **Intelligent Memory Management**
- **Semantic search** with vector embeddings
- **Natural language time queries** ("yesterday", "last week")
- **Tag-based organization** with smart categorization
- **Memory consolidation** with dream-inspired algorithms

### 🔗 **Universal Compatibility**
- **Claude Desktop** - Native MCP integration
- **Claude Code** - Memory-aware development with hooks
- **VS Code, Cursor, Continue** - IDE extensions
- **13+ AI applications** - REST API compatibility

### 💾 **Flexible Storage**
- **SQLite-vec** - Fast local storage (recommended)
- **ChromaDB** - Multi-client collaboration  
- **Cloudflare** - Global edge distribution
- **Automatic backups** and synchronization

### 🚀 **Production Ready**
- **Cross-platform** - Windows, macOS, Linux
- **Service installation** - Auto-start background operation
- **HTTPS/SSL** - Secure connections
- **Docker support** - Easy deployment

## 💡 Basic Usage

```bash
# Store a memory
uv run memory store "Fixed race condition in authentication by adding mutex locks"

# Search for relevant memories  
uv run memory recall "authentication race condition"

# Search by tags
uv run memory search --tags python debugging

# Check system health
uv run memory health
```

## 🔧 Configuration

### opencode Integration

#### Basic Configuration
Add to your opencode config (`~/.config/opencode/opencode.json`):

```json
{
  "mcpServers": {
    "memory": {
      "command": "/Users/nervkil/mcp-memory-service/venv/bin/python",
      "args": ["/Users/nervkil/mcp-memory-service/scripts/run_memory_server.py"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_HTTP_ENABLED": "false"
      }
    }
  }
}
```

#### With Custom Storage Path
```json
{
  "mcpServers": {
    "memory": {
      "command": "/Users/nervkil/mcp-memory-service/venv/bin/python",
      "args": ["/Users/nervkil/mcp-memory-service/scripts/run_memory_server.py"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PATH": "/path/to/custom/memory.db",
        "MCP_HTTP_ENABLED": "false"
      }
    }
  }
}
```

#### With HTTP API Enabled (Optional)
```json
{
  "mcpServers": {
    "memory": {
      "command": "/Users/nervkil/mcp-memory-service/venv/bin/python",
      "args": ["/Users/nervkil/mcp-memory-service/scripts/run_memory_server.py"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_HTTP_ENABLED": "true",
        "MCP_HTTP_PORT": "8000"
      }
    }
  }
}
```

### Claude Desktop Integration
Add to your Claude Desktop config (`~/.claude/config.json`):

```json
{
  "mcpServers": {
    "memory": {
      "command": "uv",
      "args": ["--directory", "/path/to/mcp-memory-service", "run", "memory", "server"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec"
      }
    }
  }
}
```

### Environment Variables
```bash
# Storage backend (sqlite_vec recommended)
export MCP_MEMORY_STORAGE_BACKEND=sqlite_vec

# Custom database path
export MCP_MEMORY_SQLITE_PATH=/path/to/memory.db

# Enable HTTP API (optional)
export MCP_HTTP_ENABLED=true
export MCP_HTTP_PORT=8000

# Security
export MCP_API_KEY="your-secure-key"

# Disable web app (recommended for pure MCP usage)
export MCP_HTTP_ENABLED=false
```

### NPX Installation

#### Install Globally via NPM
```bash
npm install -g mcp-memory-service
```

#### Basic Configuration
```json
{
  "mcpServers": {
    "memory": {
      "command": "mcp-memory-service",
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec"
      }
    }
  }
}
```

#### With Custom Database Path
```json
{
  "mcpServers": {
    "memory": {
      "command": "mcp-memory-service",
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_MEMORY_SQLITE_PATH": "/path/to/custom/memory.db"
      }
    }
  }
}
```

### Docker Installation

#### Using Pre-built Image
```bash
docker pull doobidoo/mcp-memory-service:latest
```

#### Basic Configuration
```json
{
  "mcpServers": {
    "memory": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "MCP_MEMORY_STORAGE_BACKEND=sqlite_vec",
        "doobidoo/mcp-memory-service:latest"
      ]
    }
  }
}
```

#### With Volume Mount for Persistent Storage
```json
{
  "mcpServers": {
    "memory": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/host/path/to/memory:/app/data",
        "-e", "MCP_MEMORY_SQLITE_PATH=/app/data/memory.db",
        "-e", "MCP_MEMORY_STORAGE_BACKEND=sqlite_vec",
        "doobidoo/mcp-memory-service:latest"
      ]
    }
  }
}
```

#### With HTTP API Enabled
```json
{
  "mcpServers": {
    "memory": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-p", "8000:8000",
        "-e", "MCP_MEMORY_STORAGE_BACKEND=sqlite_vec",
        "-e", "MCP_HTTP_ENABLED=true",
        "-e", "MCP_HTTP_PORT=8000",
        "doobidoo/mcp-memory-service:latest"
      ]
    }
  }
}
```

### HTTP Transport (Optional)

The server supports both STDIO (default) and HTTP transports:

#### STDIO Transport (Default)
- **Best for**: opencode and most MCP clients
- **Usage**: Automatic - no additional configuration needed

#### HTTP Transport
- **Best for**: Web-based applications and remote MCP clients
- **Usage**: Set the `MCP_HTTP_ENABLED=true` environment variable

##### HTTP Server Configuration
```json
{
  "mcpServers": {
    "memory-http": {
      "command": "/Users/nervkil/mcp-memory-service/venv/bin/python",
      "args": ["/Users/nervkil/mcp-memory-service/scripts/run_memory_server.py"],
      "env": {
        "MCP_MEMORY_STORAGE_BACKEND": "sqlite_vec",
        "MCP_HTTP_ENABLED": "true",
        "MCP_HTTP_PORT": "8000"
      }
    }
  }
}
```

**HTTP Endpoints:**
- **MCP Protocol**: `POST/GET/DELETE /mcp`
- **Health Check**: `GET /health`
- **Dashboard**: `GET /` (if web app enabled)
- **CORS**: Enabled for web clients

**Testing HTTP Server:**
```bash
# Start HTTP server
MCP_HTTP_ENABLED=true MCP_HTTP_PORT=8000 /Users/nervkil/mcp-memory-service/venv/bin/python /Users/nervkil/mcp-memory-service/scripts/run_memory_server.py

# Check health
curl http://localhost:8000/health
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Clients    │    │  MCP Protocol   │    │ Storage Backend │
│                 │    │                 │    │                 │
│ • Claude Desktop│◄──►│ • Memory Store  │◄──►│ • SQLite-vec    │
│ • Claude Code   │    │ • Semantic      │    │ • ChromaDB      │
│ • VS Code       │    │   Search        │    │ • Cloudflare    │
│ • Cursor        │    │ • Tag System    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Development

### Coding Guidelines

- Use Python type hints for type safety
- Follow existing error handling patterns with proper logging
- Keep error messages concise but informative
- Write comprehensive unit tests for new functionality
- Ensure all tests pass before submitting PRs
- Maintain test coverage above 80%
- Test changes with the MCP inspector
- Run integration tests before submitting PRs
- Document new features and configuration options
- Follow PEP 8 style guidelines

### Project Structure
```
mcp-memory-service/
├── src/mcp_memory_service/    # Core application
│   ├── models/                # Data models
│   ├── storage/               # Storage backends
│   ├── web/                   # HTTP API & dashboard
│   └── server.py              # MCP server
├── scripts/                   # Utilities & installation
├── tests/                     # Test suite
└── tools/docker/              # Docker configuration
```

### Development Workflow

#### 1. Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/vanfleet-dev/mcp-memory-service.git
cd mcp-memory-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

#### 2. Development Commands
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/mcp_memory_service --cov-report=html

# Run type checking
mypy src/mcp_memory_service

# Run linting
flake8 src/mcp_memory_service

# Format code
black src/mcp_memory_service
isort src/mcp_memory_service
```

#### 3. Testing MCP Server
```bash
# Test with MCP inspector
python -m mcp.server.stdio memory

# Run integration tests
pytest tests/integration/
```

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run the full test suite (`pytest`)
5. Ensure code formatting (`black` and `isort`)
6. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🆘 Support

- **📖 Documentation**: [Wiki](https://github.com/doobidoo/mcp-memory-service/wiki) - Comprehensive guides
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/doobidoo/mcp-memory-service/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/doobidoo/mcp-memory-service/discussions)
- **🔧 Troubleshooting**: [Troubleshooting Guide](https://github.com/doobidoo/mcp-memory-service/wiki/07-TROUBLESHOOTING)

## 📊 In Production

**Real-world metrics from active deployments:**
- **750+ memories** stored and actively used
- **<500ms response time** for semantic search
- **65% token reduction** in Claude Code sessions  
- **96.7% faster** context setup (15min → 30sec)
- **100% knowledge retention** across sessions

## 🏆 Recognition

- [![Smithery](https://smithery.ai/badge/@doobidoo/mcp-memory-service)](https://smithery.ai/server/@doobidoo/mcp-memory-service) **Verified MCP Server**
- [![Glama AI](https://img.shields.io/badge/Featured-Glama%20AI-blue)](https://glama.ai/mcp/servers/bzvl3lz34o) **Featured AI Tool**
- **Production-tested** across 13+ AI applications
- **Community-driven** with real-world feedback and improvements

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

---

**Ready to supercharge your AI workflow?** 🚀

👉 **[Start with our Installation Guide](https://github.com/doobidoo/mcp-memory-service/wiki/01-Installation-Guide)** or explore the **[Wiki](https://github.com/doobidoo/mcp-memory-service/wiki)** for comprehensive documentation.

*Transform your AI conversations into persistent, searchable knowledge that grows with you.*