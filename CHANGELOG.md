# Changelog

All notable changes to the MCP Memory Service project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-07-29

### Added
- **Claude Code Commands Integration**: 5 conversational memory commands following CCPlugins pattern
  - `/memory-store`: Store information with context and smart tagging
  - `/memory-recall`: Time-based memory retrieval with natural language
  - `/memory-search`: Tag and content-based semantic search
  - `/memory-context`: Capture current session and project context
  - `/memory-health`: Service health diagnostics and statistics
- **Optional Installation System**: Integrated command installation into main installer
  - New CLI arguments: `--install-claude-commands`, `--skip-claude-commands-prompt`
  - Intelligent prompting during installation when Claude Code CLI is detected
  - Automatic backup of existing commands with timestamps
- **Command Management Utilities**: Standalone installation and management script
  - `scripts/claude_commands_utils.py` for manual command installation
  - Cross-platform support with comprehensive error handling
  - Prerequisites testing and service connectivity validation
- **Context-Aware Operations**: Commands understand project and session context
  - Automatic project detection from current directory and git repository
  - Smart tag generation based on file types and development context
  - Session analysis and summarization capabilities
- **Auto-Discovery Integration**: Commands automatically locate MCP Memory Service
  - Uses existing mDNS service discovery functionality
  - Graceful fallback when service is unavailable
  - Backend-agnostic operation (works with both ChromaDB and SQLite-vec)

### Changed
- Updated main README.md with Claude Code commands feature documentation
- Enhanced `docs/guides/claude-code-integration.md` with comprehensive command usage guide
- Updated installation documentation to include new command options
- Version bump from 2.1.0 to 2.2.0 for significant feature addition

### Documentation
- Added detailed command descriptions and usage examples
- Created comparison guide between conversational commands and MCP server registration
- Enhanced troubleshooting documentation for both integration methods
- Added `claude_commands/README.md` with complete command reference

## [2.1.0] - 2025-07-XX

### Added
- **mDNS Service Discovery**: Zero-configuration networking with automatic service discovery
- **HTTPS Support**: SSL/TLS support with automatic self-signed certificate generation
- **Enhanced HTTP-MCP Bridge**: Auto-discovery mode with health validation and fallback
- **Zero-Config Deployment**: No manual endpoint configuration needed for local networks

### Changed
- Updated service discovery to use `_mcp-memory._tcp.local.` service type
- Enhanced HTTP server with SSL certificate generation capabilities
- Improved multi-client coordination with automatic discovery

## [2.0.0] - 2025-07-XX

### Added
- **Dream-Inspired Memory Consolidation**: Autonomous memory management system
- **Multi-layered Time Horizons**: Daily, weekly, monthly, quarterly, yearly consolidation
- **Creative Association Discovery**: Finding non-obvious connections between memories
- **Semantic Clustering**: Automatic organization of related memories
- **Intelligent Compression**: Preserving key information while reducing storage
- **Controlled Forgetting**: Safe archival and recovery systems
- **Performance Optimization**: Efficient processing of 10k+ memories
- **Health Monitoring**: Comprehensive error handling and alerts

### Changed
- Major architecture updates for consolidation system
- Enhanced storage backends with consolidation support
- Improved multi-client coordination capabilities

## [1.0.0] - 2025-07-XX

### Added
- Initial stable release
- Core memory operations (store, retrieve, search, recall)
- ChromaDB and SQLite-vec storage backends
- Cross-platform compatibility
- Claude Desktop integration
- Basic multi-client support

## [0.1.0] - 2025-07-XX

### Added
- Initial development release
- Basic memory storage and retrieval functionality
- ChromaDB integration
- MCP server implementation