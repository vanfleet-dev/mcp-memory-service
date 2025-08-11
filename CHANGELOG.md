# Changelog

All notable changes to the MCP Memory Service project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.3.2] - 2025-08-11

### 🎯 **Repository Organization & PyTorch Download Fix**

#### Fixed
- **PyTorch Repeated Downloads**: Completely resolved Claude Desktop downloading PyTorch (230MB+) on every startup
  - Root cause: UV package manager isolation prevented offline environment variables from taking effect
  - Solution: Created `scripts/memory_offline.py` launcher that sets offline mode BEFORE any imports
  - Updated Claude Desktop config to use Python directly instead of UV isolation
  - Added comprehensive offline mode configuration for HuggingFace transformers

- **Environment Variable Inheritance**: Fixed UV environment isolation issues
  - Implemented direct Python execution bypass for Claude Desktop integration
  - Added code-level offline setup in `src/mcp_memory_service/__init__.py` as fallback
  - Ensured cached model usage without network requests

#### Changed
- **Repository Structure**: Major cleanup and reorganization of root directory
  - Moved documentation files to appropriate `/docs` subdirectories
  - Consolidated guides in `docs/guides/`, technical docs in `docs/technical/`
  - Moved deployment guides to `docs/deployment/`, installation to `docs/installation/`
  - Removed obsolete debug scripts and development notes
  - Moved service management scripts to `/scripts` directory

- **Documentation Organization**: Improved logical hierarchy
  - Claude Code compatibility → `docs/guides/claude-code-compatibility.md`
  - Setup guides → `docs/installation/` and `docs/guides/`
  - Technical documentation → `docs/technical/`
  - Integration guides → `docs/integrations/`

#### Technical Details
- **Offline Mode Implementation**: `scripts/memory_offline.py` sets `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` before ML library imports
- **Config Optimization**: Updated Claude Desktop config templates for both Windows and general use
- **Cache Management**: Proper Windows cache path configuration for sentence-transformers and HuggingFace

#### Impact
- ✅ **Eliminated 230MB PyTorch downloads** - Startup time reduced from ~60s to ~3s
- ✅ **Professional repository structure** - Clean root directory with logical documentation hierarchy  
- ✅ **Improved maintainability** - Consolidated scripts and removed redundant files
- ✅ **Enhanced user experience** - No more frustrating download delays in Claude Desktop

This release resolves the persistent PyTorch download issue that affected Windows users and establishes a clean, professional repository structure suitable for enterprise deployment.

## [4.3.1] - 2025-08-11

### 🔧 **Critical Windows Installation Fixes**

#### Fixed
- **PyTorch-DirectML Compatibility**: Resolved major installation issues on Windows 11
  - Fixed installer attempting to install incompatible PyTorch 2.5.1 over working 2.4.1+DirectML setup
  - Added smart compatibility checking: PyTorch 2.4.x works with DirectML, 2.5.x doesn't
  - Enhanced `install_pytorch_windows()` to preserve existing compatible installations
  - Only installs torch-directml if PyTorch 2.4.1 exists without DirectML extensions
  
- **Corrupted Virtual Environment Recovery**: Fixed "module 'torch' has no attribute 'version'" errors
  - Implemented complete cleanup of corrupted `~orch` and `functorch` directories  
  - Added robust uninstall and reinstall process for broken PyTorch installations
  - Restored proper torch.version attribute functionality
  
- **Windows 11 Detection**: Fixed incorrect OS identification
  - Implemented registry-based Windows 11 detection using build numbers (≥22000)
  - Replaced unreliable platform detection with accurate registry lookups
  - Added system info caching to prevent duplicate detection calls

- **Installation Logging Improvements**: Enhanced installer feedback and debugging
  - Created built-in DualOutput logging system with UTF-8 encoding
  - Fixed character encoding issues in installation logs
  - Added comprehensive logging for PyTorch compatibility decisions

#### Changed
- **Installation Intelligence**: Installer now preserves working DirectML setups instead of force-upgrading
- **Error Prevention**: Added extensive pre-checks to prevent corrupted package installations
- **User Experience**: Clear messaging about PyTorch version compatibility and preservation decisions

#### Technical Details
- Enhanced PyTorch version detection and compatibility matrix
- Smart preservation of PyTorch 2.4.1 + torch-directml 0.2.5.dev240914 combinations
- Automatic cleanup of corrupted package directories during installation recovery
- Registry-based Windows version detection via `SOFTWARE\Microsoft\Windows NT\CurrentVersion`

This release resolves critical Windows installation failures that prevented successful PyTorch-DirectML setup, ensuring reliable DirectML acceleration on Windows 11 systems.

## [4.3.0] - 2025-08-10

### ⚡ **Developer Experience Improvements**

#### Added
- **Automated uv.lock Conflict Resolution**: Eliminates manual merge conflict resolution
  - Custom git merge driver automatically resolves `uv.lock` conflicts
  - Auto-runs `uv sync` after conflict resolution to ensure consistency
  - One-time setup script for contributors: `./scripts/setup-git-merge-drivers.sh`
  - Comprehensive documentation in README.md and CLAUDE.md

#### Technical
- Added `.gitattributes` configuration for `uv.lock` merge handling
- Created `scripts/uv-lock-merge.sh` custom merge driver script
- Added contributor setup script with automatic git configuration
- Enhanced development documentation with git setup instructions

This release significantly improves the contributor experience by automating the resolution of the most common merge conflicts in the repository.

## [4.2.0] - 2025-08-10

### 🔧 **Improved Client Compatibility**

#### Added
- **LM Studio Compatibility Layer**: Automatic handling of non-standard MCP notifications
  - Monkey patch for `notifications/cancelled` messages that aren't in the MCP specification
  - Graceful error handling prevents server crashes when LM Studio cancels operations
  - Debug logging for troubleshooting compatibility issues
  - Comprehensive documentation in `docs/LM_STUDIO_COMPATIBILITY.md`

#### Technical
- Added `lm_studio_compat.py` module with compatibility patches
- Applied patches automatically during server initialization
- Enhanced error handling in MCP protocol communication

This release significantly improves compatibility with LM Studio and other MCP clients while maintaining full backward compatibility with existing Claude Desktop integrations.

## [4.1.1] - 2025-08-10

### Fixed
- **macOS ARM64 Support**: Enhanced PyTorch installation for Apple Silicon
  - Proper dependency resolution for M1/M2/M3 Mac systems
  - Updated torch dependency requirements from `>=1.6.0` to `>=2.0.0` in `pyproject.toml`
  - Platform-specific installation instructions in `install.py`
  - Improved cross-platform dependency management

## [4.1.0] - 2025-08-06

### 🎯 **Full MCP Specification Compliance**

#### Added
- **Enhanced Resources System**: URI-based access to memory collections
  - `memory://stats` - Real-time database statistics and health metrics
  - `memory://tags` - Complete list of available memory tags
  - `memory://recent/{n}` - Access to N most recent memories
  - `memory://tag/{tagname}` - Query memories by specific tag
  - `memory://search/{query}` - Dynamic search with structured results
  - Resource templates for parameterized queries
  - JSON responses for all resource endpoints

- **Guided Prompts Framework**: Interactive workflows for memory operations
  - `memory_review` - Review and organize memories from specific time periods
  - `memory_analysis` - Analyze patterns, themes, and tag distributions
  - `knowledge_export` - Export memories in JSON, Markdown, or Text formats
  - `memory_cleanup` - Identify and remove duplicate or outdated memories
  - `learning_session` - Store structured learning notes with automatic categorization
  - Each prompt includes proper argument schemas and validation

- **Progress Tracking System**: Real-time notifications for long operations
  - Progress notifications with percentage completion
  - Operation IDs for tracking concurrent tasks
  - Enhanced `delete_by_tags` with step-by-step progress
  - Enhanced `dashboard_optimize_db` with operation stages
  - MCP-compliant progress notification protocol

#### Changed
- Extended `MemoryStorage` base class with helper methods for resources
- Enhanced `Memory` and `MemoryQueryResult` models with `to_dict()` methods
- Improved server initialization with progress tracking state management

#### Technical
- Added `send_progress_notification()` method to MemoryServer
- Implemented `get_stats()`, `get_all_tags()`, `get_recent_memories()` in storage base
- Full backward compatibility maintained with existing operations

This release brings the MCP Memory Service to full compliance with the Model Context Protocol specification, enabling richer client interactions and better user experience through structured data access and guided workflows.

## [4.0.1] - 2025-08-04

### Fixed
- **MCP Protocol Validation**: Resolved critical ID validation errors affecting integer/string ID handling
- **Embedding Model Loading**: Fixed model loading failures in offline environments
- **Semantic Search**: Restored semantic search functionality that was broken in 4.0.0
- **Version Consistency**: Fixed version mismatch between `__init__.py` and `pyproject.toml`

### Technical
- Enhanced flexible ID validation for MCP protocol compliance
- Improved error handling for embedding model initialization
- Corrected version bumping process for patch releases

## [4.0.0] - 2025-08-04

### 🚀 **Major Release: Production-Ready Remote MCP Memory Service**

#### Added
- **Native MCP-over-HTTP Protocol**: Direct MCP protocol support via FastAPI without Node.js bridge
- **Remote Server Deployment**: Full production deployment capability with remote access
- **Cross-Device Memory Access**: Validated multi-device memory synchronization
- **Comprehensive Documentation**: Complete deployment guides and remote access documentation

#### Changed
- **Architecture Evolution**: Transitioned from local experimental service to production infrastructure
- **Protocol Compliance**: Applied MCP protocol refactorings with flexible ID validation
- **Docker CI/CD**: Fixed and operationalized Docker workflows for automated deployment
- **Repository Maintenance**: Comprehensive cleanup and branch management

#### Production Validation
- Successfully deployed server running at remote endpoints with 65+ memories
- SQLite-vec backend validated (1.7MB database, 384-dim embeddings)
- all-MiniLM-L6-v2 model loaded and operational
- Full MCP tool suite available and tested

#### Milestones Achieved
- GitHub Issue #71 (remote access) completed
- GitHub Issue #72 (bridge deprecation) resolved
- Production deployment proven successful

## [4.0.0-beta.1] - 2025-08-03

### Added
- **Dual-Service Architecture**: Combined HTTP Dashboard + Native MCP Protocol
- **FastAPI MCP Integration**: Complete integration for native remote access
- **Direct MCP-over-HTTP**: Eliminated dependency on Node.js bridge

### Changed
- **Remote Access Solution**: Resolved remote memory service access (Issue #71)
- **Bridge Deprecation**: Deprecated Node.js bridge in favor of direct protocol
- **Docker Workflows**: Fixed CI/CD pipeline for automated testing

### Technical
- Maintained backward compatibility for existing HTTP API users
- Repository cleanup and branch management improvements
- Significant architectural evolution while preserving existing functionality

## [4.0.0-alpha.1] - 2025-08-03

### Added
- **Initial FastAPI MCP Server**: First implementation of native MCP server structure
- **MCP Protocol Endpoints**: Added core MCP protocol endpoints to FastAPI server
- **Hybrid Support**: Initial HTTP+MCP hybrid architecture support

### Changed
- **Server Architecture**: Began transition from pure HTTP to MCP-native implementation
- **Remote Access Configuration**: Initial configuration for remote server access
- **Protocol Implementation**: Started implementing MCP specification compliance

### Technical
- Validated local testing with FastAPI MCP server
- Fixed `mcp.run()` syntax issues
- Established foundation for dual-protocol support

## [3.3.4] - 2025-08-03

### Fixed
- **Multi-Client Backend Selection**: Fixed hardcoded sqlite_vec backend in multi-client configuration
  - Configuration functions now properly accept and use storage_backend parameter
  - Chosen backend is correctly passed through entire multi-client setup flow
  - M1 Macs with MPS acceleration now correctly use ChromaDB when selected
  - SQLite pragmas only applied when sqlite_vec is actually chosen

### Changed
- **Configuration Instructions**: Updated generic configuration to reflect chosen backend
- **Backend Flexibility**: All systems now get optimal backend configuration in multi-client mode

### Technical
- Resolved Issue #73 affecting M1 Mac users
- Ensures proper backend-specific configuration for all platforms
- Version bump to 3.3.4 for critical fix release

## [3.3.3] - 2025-08-02

### 🔒 **SSL Certificate & MCP Bridge Compatibility**

#### Fixed
- **SSL Certificate Generation**: Now generates certificates with proper Subject Alternative Names (SANs) for multi-hostname/IP compatibility
  - Auto-detects local machine IP address dynamically (no hardcoded IPs)
  - Includes `DNS:memory.local`, `DNS:localhost`, `DNS:*.local` 
  - Includes `IP:127.0.0.1`, `IP:::1` (IPv6), and auto-detected local IP
  - Environment variable support: `MCP_SSL_ADDITIONAL_IPS`, `MCP_SSL_ADDITIONAL_HOSTNAMES`
- **Node.js MCP Bridge Compatibility**: Resolved SSL handshake failures when connecting from Claude Code
  - Added missing MCP protocol methods: `initialize`, `tools/list`, `tools/call`, `notifications/initialized`
  - Enhanced error handling with exponential backoff retry logic (3 attempts, max 5s delay)
  - Comprehensive request/response logging with unique request IDs
  - Improved HTTPS client configuration with custom SSL agent
  - Reduced timeout from 30s to 10s for faster failure detection
  - Removed conflicting Host headers that caused SSL verification issues

#### Changed
- **Certificate Security**: CN changed from `localhost` to `memory.local` for better hostname matching
- **HTTP Client**: Enhanced connection management with explicit port handling and connection close headers
- **Logging**: Added detailed SSL handshake and request flow debugging

#### Environment Variables
- `MCP_SSL_ADDITIONAL_IPS`: Comma-separated list of additional IP addresses to include in certificate
- `MCP_SSL_ADDITIONAL_HOSTNAMES`: Comma-separated list of additional hostnames to include in certificate

This release resolves SSL connectivity issues that prevented Claude Code from connecting to remote MCP Memory Service instances across different networks and deployment environments.

## [3.0.0] - 2025-07-29

### 🚀 MAJOR RELEASE: Autonomous Multi-Client Memory Service

This is a **major architectural evolution** transforming MCP Memory Service from a development tool into a production-ready, intelligent memory system with autonomous processing capabilities.

### Added
#### 🧠 **Dream-Inspired Consolidation System**
- **Autonomous Memory Processing**: Fully autonomous consolidation system inspired by human cognitive processes
- **Exponential Decay Scoring**: Memory aging with configurable retention periods (critical: 365d, reference: 180d, standard: 30d, temporary: 7d)
- **Creative Association Discovery**: Automatic discovery of semantic connections between memories (similarity range 0.3-0.7)
- **Semantic Clustering**: DBSCAN algorithm for intelligent memory grouping (minimum 5 memories per cluster)
- **Memory Compression**: Statistical summarization with 500-character limits while preserving originals
- **Controlled Forgetting**: Relevance-based memory archival system (threshold 0.1, 90-day access window)
- **Automated Scheduling**: Configurable consolidation schedules (daily 2AM, weekly Sunday 3AM, monthly 1st 4AM)
- **Zero-AI Dependencies**: Operates entirely offline using existing embeddings and mathematical algorithms

#### 🌐 **Multi-Client Server Architecture**
- **HTTPS Server**: Production-ready FastAPI server with auto-generated SSL certificates
- **mDNS Service Discovery**: Zero-configuration automatic service discovery (`MCP Memory._mcp-memory._tcp.local.`)
- **Server-Sent Events (SSE)**: Real-time updates with 30s heartbeat intervals for all connected clients
- **Multi-Interface Support**: Service advertisement across all network interfaces (WiFi, Ethernet, Docker, etc.)
- **API Authentication**: Secure API key-based authentication system
- **Cross-Platform Discovery**: Works on Windows, macOS, and Linux with standard mDNS/Bonjour

#### 🚀 **Production Deployment System**
- **Systemd Auto-Startup**: Complete systemd service integration for automatic startup on boot
- **Service Management**: Professional service control scripts with start/stop/restart/status/logs/health commands
- **User-Space Service**: Runs as regular user (not root) for enhanced security
- **Auto-Restart**: Automatic service recovery on failures with 10-second restart delay
- **Journal Logging**: Integrated with systemd journal for professional log management
- **Health Monitoring**: Built-in health checks and monitoring endpoints

#### 📖 **Comprehensive Documentation**
- **Complete Setup Guide**: 100+ line comprehensive production deployment guide
- **Production Quick Start**: Streamlined production deployment instructions
- **Service Management**: Full service lifecycle documentation
- **Troubleshooting**: Detailed problem resolution guides
- **Network Configuration**: Firewall and mDNS setup instructions

### Enhanced
#### 🔧 **Improved Server Features**
- **Enhanced SSE Implementation**: Restored full Server-Sent Events functionality with connection statistics
- **Network Optimization**: Multi-interface service discovery and connection handling
- **Configuration Management**: Environment-based configuration with secure defaults
- **Error Handling**: Comprehensive error handling and recovery mechanisms

#### 🛠️ **Developer Experience**
- **Debug Tools**: Service debugging and testing utilities
- **Installation Scripts**: One-command installation and configuration
- **Management Scripts**: Easy service lifecycle management
- **Archive Organization**: Clean separation of development and production files

### Configuration
#### 🔧 **New Environment Variables**
- `MCP_CONSOLIDATION_ENABLED`: Enable/disable autonomous consolidation (default: true)
- `MCP_MDNS_ENABLED`: Enable/disable mDNS service discovery (default: true)
- `MCP_MDNS_SERVICE_NAME`: Customizable service name for discovery (default: "MCP Memory")
- `MCP_HTTPS_ENABLED`: Enable HTTPS with auto-generated certificates (default: true)
- `MCP_HTTP_HOST`: Server bind address (default: 0.0.0.0 for multi-client)
- `MCP_HTTP_PORT`: Server port (default: 8000)
- Consolidation timing controls: `MCP_SCHEDULE_DAILY`, `MCP_SCHEDULE_WEEKLY`, `MCP_SCHEDULE_MONTHLY`

### Breaking Changes
- **Architecture Change**: Single-client MCP protocol → Multi-client HTTPS server architecture
- **Service Discovery**: Manual configuration → Automatic mDNS discovery
- **Deployment Model**: Development script → Production systemd service
- **Access Method**: Direct library import → HTTP API with authentication

### Migration
- **Client Configuration**: Update to use HTTP-MCP bridge with auto-discovery
- **Service Deployment**: Install systemd service for production use
- **Network Setup**: Configure firewall for ports 8000/tcp (HTTPS) and 5353/udp (mDNS)
- **API Access**: Use generated API key for authentication

### Technical Details
- **Consolidation Algorithm**: Mathematical approach using existing embeddings without external AI
- **Service Architecture**: FastAPI + uvicorn + systemd for production deployment
- **Discovery Protocol**: RFC-compliant mDNS service advertisement
- **Security**: User-space execution, API key authentication, HTTPS encryption
- **Storage**: Continues to support both ChromaDB and SQLite-vec backends

---

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