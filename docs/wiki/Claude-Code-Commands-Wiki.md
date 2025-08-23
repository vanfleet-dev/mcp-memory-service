# Claude Code Commands - Complete Wiki Guide

*This content is designed for the GitHub Wiki. Copy and paste sections as needed.*

---

## Home Page Content

### MCP Memory Service - Claude Code Commands

**Transform your Claude Code experience with persistent memory capabilities!**

The MCP Memory Service now offers **conversational Claude Code commands** that provide direct access to powerful memory operations without any MCP server configuration.

#### 🚀 Quick Start
```bash
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service
python install.py --install-claude-commands
claude /memory-health  # Test it works!
```

#### 📚 Wiki Contents
- **[Installation Guide](#installation-guide)** - Complete setup instructions
- **[Command Reference](#command-reference)** - All 5 commands with examples
- **[Memory Awareness Hooks](#memory-awareness-hooks)** - Automatic background memory system
- **[Usage Examples](#usage-examples)** - Real-world workflows
- **[Commands vs MCP Server vs Hooks](#commands-vs-mcp-server-vs-hooks)** - Which approach to choose
- **[Troubleshooting](#troubleshooting)** - Common issues and solutions
- **[Advanced Features](#advanced-features)** - Power user capabilities

---

## Installation Guide

### Prerequisites
- ✅ Claude Code CLI installed and working (`claude --version`)
- ✅ Python 3.10+ with pip
- ✅ Git for cloning the repository

### Method 1: Integrated Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/doobidoo/mcp-memory-service.git
cd mcp-memory-service

# Install with Claude Code commands
python install.py --install-claude-commands
```

**What this does:**
- Detects your system and optimizes installation
- Installs MCP Memory Service with best backend for your hardware
- Automatically detects Claude Code CLI
- Installs 5 conversational memory commands
- Creates backup of existing commands
- Tests everything to ensure it works

### Method 2: Commands Only
```bash
# If you already have MCP Memory Service installed
python scripts/claude_commands_utils.py

# Test installation
python scripts/claude_commands_utils.py --test
```

### Method 3: Manual Installation
```bash
# Install commands to specific location
cp claude_commands/*.md ~/.claude/commands/

# Verify installation
ls ~/.claude/commands/memory-*.md
```

### Installation Options
- `--skip-claude-commands-prompt` - Skip interactive prompts
- `--install-claude-commands` - Force install commands
- See [Installation Master Guide](../installation/master-guide.md) for all options

---

## Command Reference

### `/memory-store` - Store Information with Context

**Purpose**: Store information in your memory service with automatic context detection and smart tagging.

**Basic Usage**:
```bash
claude /memory-store "Important architectural decision about database backend"
```

**Advanced Usage**:
```bash
claude /memory-store --tags "decision,architecture" "We chose SQLite-vec for performance reasons"
claude /memory-store --type "note" --project "my-app" "Remember to update Docker config"
claude /memory-store --private "Sensitive information about deployment"
```

**Arguments**:
- `content` - The information to store (required)
- `--tags "tag1,tag2"` - Explicit tags to add
- `--type "note|decision|task|reference"` - Memory type classification
- `--project "name"` - Override automatic project detection
- `--private` - Mark as private/sensitive content

**Automatic Features**:
- ✅ Project context detection from current directory
- ✅ Git repository information capture
- ✅ Smart tag generation based on file types and patterns
- ✅ Timestamp and session metadata

---

### `/memory-recall` - Time-based Memory Retrieval

**Purpose**: Retrieve memories using natural language time expressions and contextual queries.

**Basic Usage**:
```bash
claude /memory-recall "what did we decide about the database last week?"
```

**Time Expression Examples**:
```bash
claude /memory-recall "yesterday's architectural decisions"
claude /memory-recall "memories from when we were working on authentication"
claude /memory-recall "what happened two months ago?"
claude /memory-recall "decisions made last Tuesday morning"
```

**Advanced Usage**:
```bash
claude /memory-recall --project "mcp-memory-service" "last month's progress"
claude /memory-recall --limit 20 "recent development decisions"
claude /memory-recall --tags "architecture" "planning from last week"
```

**Arguments**:
- `query` - Time-based or contextual query (required)
- `--limit N` - Maximum memories to retrieve (default: 10)
- `--project "name"` - Filter by specific project
- `--tags "tag1,tag2"` - Additional tag filtering
- `--type "note|decision|task"` - Filter by memory type
- `--include-context` - Show full session context

**Supported Time Expressions**:
- **Relative**: "yesterday", "last week", "two days ago", "this month"
- **Seasonal**: "last summer", "this winter", "spring 2024"
- **Event-based**: "before the refactor", "since we switched databases"
- **Specific**: "January 15th", "last Tuesday morning"

---

### `/memory-search` - Tag and Content Search

**Purpose**: Search through stored memories using tags, content keywords, and semantic similarity.

**Basic Usage**:
```bash
claude /memory-search --tags "architecture,database"
claude /memory-search "SQLite performance optimization"
```

**Search Types**:
```bash
# Tag-based search
claude /memory-search --tags "decision"
claude /memory-search --tags "architecture,performance,database"

# Content-based semantic search
claude /memory-search "database performance issues"
claude /memory-search "authentication implementation details"

# Combined search
claude /memory-search --tags "decision" --content "database backend"
claude /memory-search --project "my-app" --type "note" "configuration"
```

**Advanced Usage**:
```bash
claude /memory-search --limit 50 --min-score 0.8 "database optimization"
claude /memory-search --include-metadata --export "architecture decisions"
```

**Arguments**:
- `query` - Search query (content or primary terms)
- `--tags "tag1,tag2"` - Search by specific tags
- `--content "text"` - Explicit content search terms
- `--project "name"` - Filter by project name
- `--type "note|decision|task|reference"` - Filter by memory type
- `--limit N` - Maximum results (default: 20)
- `--min-score 0.X` - Minimum relevance threshold
- `--include-metadata` - Show full metadata
- `--export` - Export results to file

**Search Features**:
- ✅ Semantic similarity using embeddings
- ✅ Fuzzy matching for typos
- ✅ Tag-based filtering with partial matching
- ✅ Relevance scoring and ranking
- ✅ Context highlighting

---

### `/memory-context` - Session Context Integration

**Purpose**: Capture the current conversation and project context as a memory for future reference.

**Basic Usage**:
```bash
claude /memory-context
```

**With Custom Summary**:
```bash
claude /memory-context --summary "Architecture planning session for OAuth integration"
claude /memory-context --tags "planning,oauth" --type "session"
```

**Advanced Usage**:
```bash
claude /memory-context --include-files --include-commits
claude /memory-context --private --project "secret-project"
```

**Arguments**:
- `--summary "text"` - Custom session summary
- `--tags "tag1,tag2"` - Additional tags to apply
- `--type "session|meeting|planning|development"` - Context type
- `--include-files` - Include detailed file change information
- `--include-commits` - Include recent commit messages
- `--include-code` - Include code change snippets
- `--private` - Mark as private/sensitive content
- `--project "name"` - Override project detection

**Automatic Capture**:
- ✅ Conversation analysis and key topic extraction
- ✅ Git repository state and recent commits
- ✅ Current directory and project context
- ✅ Development session insights and decisions
- ✅ Action items and next steps identification

---

### `/memory-health` - Service Health and Diagnostics

**Purpose**: Check the health and status of your MCP Memory Service with comprehensive diagnostics.

**Basic Usage**:
```bash
claude /memory-health
```

**Detailed Diagnostics**:
```bash
claude /memory-health --detailed
claude /memory-health --test-operations
claude /memory-health --performance-test
```

**Advanced Features**:
```bash
claude /memory-health --check-backups
claude /memory-health --export-report
claude /memory-health --fix-issues
```

**Arguments**:
- `--detailed` - Show comprehensive diagnostics
- `--test-operations` - Test store/retrieve functionality
- `--check-backups` - Verify backup system health
- `--performance-test` - Run performance benchmarks
- `--export-report` - Save health report to file
- `--fix-issues` - Attempt automatic fixes
- `--quiet` - Show only critical issues

**Health Report Includes**:
- ✅ Service connectivity and response times
- ✅ Database health and statistics
- ✅ Storage backend configuration
- ✅ Memory count and usage patterns
- ✅ Performance metrics and bottlenecks
- ✅ Common issue detection and fixes

---

## Memory Awareness Hooks

### Overview - Automatic Background Memory System

**Memory Awareness Hooks** transform Claude Code into a **memory-aware development assistant** that automatically maintains perfect context across all interactions without any manual intervention.

Unlike commands that require explicit user actions, hooks work **transparently in the background** during your Claude Code sessions:

- 🚀 **Session Start**: Automatically loads relevant project memories when Claude Code starts
- 🧠 **Dynamic Context**: Real-time memory injection based on conversation evolution  
- 📝 **Session End**: Automatically consolidates and stores conversation outcomes
- 🎯 **Project Awareness**: Intelligent project context detection and memory relevance scoring

#### How It Works
1. **You start Claude Code** → Hook detects project, loads relevant memories, injects as context
2. **You have conversations** → Claude Code operates with full historical context
3. **You end the session** → Hook analyzes outcomes, stores insights with smart tags
4. **Next session** → Previous insights are available automatically

**Result**: Every Claude Code session builds upon all previous work with zero manual effort.

---

### Hooks Installation Guide

#### Prerequisites
- ✅ Claude Code CLI installed and working
- ✅ MCP Memory Service running (any backend)
- ✅ Node.js for hook script execution

#### Installation Methods

**Method 1: Automatic Installation (Recommended)**
```bash
cd /path/to/mcp-memory-service
cd claude-hooks
./install.sh
```

**Method 2: Manual Installation**  
```bash
# Copy hooks to Claude Code directory
cp -r claude-hooks/* ~/.claude-code/hooks/

# Configure memory service endpoint
cd ~/.claude-code/hooks
cp config.template.json config.json
# Edit config.json with your memory service details
```

**Method 3: During MCP Memory Service Installation**
```bash
python install.py --install-claude-hooks
```

#### Post-Installation Verification
```bash
# Check hooks are installed
ls ~/.claude-code/hooks/core/

# Test hook functionality
cd ~/.claude-code/hooks
npm test

# Verify project detection
node -e "
const { detectProjectContext } = require('./utilities/project-detector');
detectProjectContext('.').then(console.log).catch(console.error);
"
```

---

### Hooks Configuration Reference

#### Core Configuration (`~/.claude-code/hooks/config.json`)

```json
{
  "memoryService": {
    "endpoint": "https://your-memory-service:8443",
    "apiKey": "your-api-key",
    "defaultTags": ["claude-code", "auto-generated"],
    "maxMemoriesPerSession": 8,
    "enableSessionConsolidation": true
  },
  "hooks": {
    "sessionStart": {
      "enabled": true,
      "timeout": 10000,
      "priority": "high"
    },
    "sessionEnd": {
      "enabled": true, 
      "timeout": 15000,
      "priority": "normal"
    },
    "topicChange": {
      "enabled": false,
      "timeout": 5000, 
      "priority": "low"
    }
  }
}
```

#### Project Detection Settings
```json
{
  "projectDetection": {
    "gitRepository": true,
    "packageFiles": ["package.json", "pyproject.toml", "Cargo.toml", "go.mod"],
    "frameworkDetection": true,
    "languageDetection": true,
    "confidenceThreshold": 0.3
  }
}
```

#### Memory Scoring Configuration  
```json
{
  "memoryScoring": {
    "weights": {
      "timeDecay": 0.3,
      "tagRelevance": 0.4, 
      "contentRelevance": 0.2,
      "typeBonus": 0.1
    },
    "minRelevanceScore": 0.3,
    "timeDecayRate": 0.1
  }
}
```

#### Session Analysis Settings
```json
{
  "sessionAnalysis": {
    "extractTopics": true,
    "extractDecisions": true,
    "extractInsights": true,
    "extractCodeChanges": true,
    "extractNextSteps": true,
    "minSessionLength": 100,
    "minConfidence": 0.1
  }
}
```

---

### Hook Components Architecture

#### Core Hooks
- **`session-start.js`**: Automatic memory injection at Claude Code initialization
- **`session-end.js`**: Memory consolidation and outcome storage at session completion  
- **`topic-change.js`**: Dynamic memory loading based on conversation evolution (optional)

#### Utilities
- **`project-detector.js`**: Multi-language project context detection and analysis
- **`memory-scorer.js`**: AI-powered relevance scoring algorithms for memory selection
- **`context-formatter.js`**: Memory formatting and presentation for Claude Code injection
- **`session-tracker.js`**: Session state management and conversation analysis
- **`conversation-analyzer.js`**: Natural language processing for session insights

#### Advanced Features
- **Cross-Session Continuity**: Links conversations across different Claude Code sessions
- **Intelligent Memory Selection**: Relevance scoring based on project context and time decay
- **Auto-Tagging**: Automatic categorization based on project type and content analysis
- **Knowledge Building**: Progressive memory organization and cross-linking

---

### Automatic Features in Detail

#### Session Startup Memory Injection

When you start Claude Code, the session-start hook:

1. **Detects Current Project**: Analyzes directory, git repo, package files
2. **Queries Memory Service**: Searches for relevant memories using project context
3. **Scores Memory Relevance**: Uses AI algorithms to rank memory importance
4. **Formats Context**: Prepares memories for injection into Claude Code session
5. **Injects Seamlessly**: Adds context without user awareness

**Example Auto-Generated Context**:
```
# Project Context: mcp-memory-service
Recent memories relevant to your current work:

## Architecture Decisions (2 days ago)
- Chose SQLite-vec backend for performance reasons
- Cloudflare backend ready for production deployment

## Development Notes (1 week ago)  
- Memory consolidation hooks working correctly
- Session analysis extracting topics and decisions

## Configuration (3 days ago)
- Updated config.json with new scoring weights
- Enabled session consolidation by default
```

#### Project Detection Examples

**Python Project**:
```json
{
  "name": "mcp-memory-service",
  "language": "Python",
  "frameworks": ["FastAPI"],  
  "tools": ["uv", "pytest"],
  "git": {
    "branch": "main",
    "remoteUrl": "https://github.com/user/mcp-memory-service.git"
  },
  "confidence": 0.95
}
```

**JavaScript Project**:
```json
{
  "name": "my-react-app",
  "language": "JavaScript", 
  "frameworks": ["React", "Next.js"],
  "tools": ["npm", "webpack"],
  "git": {
    "branch": "feature/auth-system"
  },
  "confidence": 0.87
}
```

#### Session End Consolidation

When Claude Code sessions end, the session-end hook:

1. **Analyzes Conversation**: Extracts topics, decisions, insights, next steps
2. **Identifies Key Information**: Uses NLP to find important outcomes  
3. **Generates Smart Tags**: Based on content, project type, and conversation topics
4. **Stores Automatically**: Creates memories without user intervention
5. **Links Context**: Connects to previous related memories

**Example Auto-Stored Memory**:
```json
{
  "content": "Session focused on implementing OAuth authentication. Decided to use Auth0 with JWT tokens. Next steps: configure environment variables and test authentication flow.",
  "tags": ["claude-code", "oauth", "auth0", "jwt", "authentication", "session-outcome"],
  "metadata": {
    "type": "session-consolidation",
    "project": "my-web-app", 
    "session_duration": "45 minutes",
    "topics": ["authentication", "oauth", "jwt"],
    "decisions": ["use Auth0", "JWT tokens"],
    "next_steps": ["configure env vars", "test auth flow"]
  }
}
```

---

### Hooks Troubleshooting

#### Hooks Not Working

**Issue**: No automatic memory injection or consolidation

```bash
# Check if hooks are installed
ls ~/.claude-code/hooks/core/

# Check configuration
cat ~/.claude-code/hooks/config.json

# Test memory service connectivity  
curl -k https://your-memory-service:8443/api/health

# Test project detection
cd ~/.claude-code/hooks
node -e "
const { detectProjectContext } = require('./utilities/project-detector');
detectProjectContext('.').then(console.log).catch(console.error);
"
```

**Common Solutions**:
- Ensure Claude Code hooks directory exists: `mkdir -p ~/.claude-code/hooks`
- Verify config.json has correct memory service endpoint
- Check memory service is running and accessible
- Ensure Node.js is available for hook execution

#### Memory Service Connection Issues

**Issue**: Hooks can't connect to memory service

```bash
# Test direct connection
curl -k -X POST https://your-service:8443/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "check_database_health", "arguments": {}}}'

# Update config with correct endpoint
nano ~/.claude-code/hooks/config.json

# Test with debug logging
export CLAUDE_HOOKS_DEBUG=true
# Start Claude Code to see debug output
```

#### Hook Execution Issues

**Issue**: Hooks installed but not executing

```bash
# Check hook permissions
ls -la ~/.claude-code/hooks/core/

# Test hook loading
cd ~/.claude-code/hooks
node -e "
try {
  const hook = require('./core/session-start.js');
  console.log('Hook loaded:', hook.name);
} catch (err) {
  console.error('Error loading hook:', err.message);
}
"

# Check for Node.js issues
node --version  # Should be v14+
npm --version   # Should be available
```

#### Performance Issues

**Issue**: Hooks causing slow Claude Code startup

```bash
# Enable performance debugging
export CLAUDE_HOOKS_DEBUG=true
export CLAUDE_HOOKS_TIMING=true

# Reduce memory injection
# Edit ~/.claude-code/hooks/config.json:
"maxMemoriesPerSession": 3,  # Reduce from default 8

# Increase timeouts if needed
"sessionStart": {
  "timeout": 15000  # Increase from 10000
}

# Disable topic-change hook if enabled
"topicChange": {
  "enabled": false
}
```

#### Configuration Issues

**Issue**: Hooks using wrong configuration

```bash
# Reset to default configuration
cd ~/.claude-code/hooks
cp config.template.json config.json

# Validate JSON configuration
cat config.json | python -m json.tool

# Check for common config errors:
# - Wrong memory service endpoint URL
# - Invalid API key format
# - Malformed JSON syntax
# - Missing required configuration sections
```

---

## Usage Examples

### Individual Developer Workflow
```bash
# Start your development day
claude /memory-context --summary "Starting work on user authentication feature"

# Store important decisions as you work
claude /memory-store --tags "auth,security" "Decided to use JWT tokens with 24h expiry"
claude /memory-store --tags "database,schema" "Added user_sessions table with token_hash column"

# Store configuration details
claude /memory-store --type "reference" "Auth0 client ID: app_123xyz (dev environment)"

# Later, recall what you decided
claude /memory-recall "what did we decide about authentication yesterday?"
claude /memory-search --tags "auth,jwt" 

# End of day - capture the session
claude /memory-context --summary "Completed JWT authentication implementation"
```

### Team Collaboration
```bash
# Before team meeting
claude /memory-recall "what architecture decisions did we make last week?"

# After team meeting
claude /memory-store --tags "team,decision" "Team agreed to migrate to microservices architecture by Q2"

# Reference team decisions
claude /memory-search --tags "team,decision" --limit 10
```

### Project Management
```bash
# Track project milestones
claude /memory-store --tags "milestone,completed" "Authentication module completed on schedule"

# Review project progress
claude /memory-recall "what milestones did we complete this month?"
claude /memory-search --tags "milestone" --type "note"

# Plan next sprint
claude /memory-recall "what blockers did we identify last week?"
```

### Learning and Documentation
```bash
# Store learning insights
claude /memory-store --tags "learning,react" "React useEffect cleanup prevents memory leaks"

# Build knowledge base
claude /memory-store --type "reference" --tags "cheatsheet,docker" "docker-compose up -d starts services in background"

# Recall knowledge
claude /memory-search "React hooks best practices"
claude /memory-recall "what did I learn about Docker last month?"
```

### Memory Awareness Hooks Workflows

#### Seamless Development Continuity

**With Hooks Enabled** (Zero Manual Effort):
```bash
# Day 1: Start Claude Code in project directory
# → Hook automatically injects: "No previous memories found for this project"
# → You work on authentication feature, make decisions
# → End session: Hook automatically stores outcomes with tags

# Day 2: Start Claude Code in same project
# → Hook automatically injects: "Yesterday you worked on authentication, decided to use JWT..."
# → You continue work with full context
# → Make new decisions about database schema
# → End session: Hook consolidates and links to previous work

# Day 3: Start Claude Code
# → Hook automatically injects: "Project progress: auth complete, working on DB schema..."
# → Perfect continuity, no manual memory management needed
```

#### Cross-Project Intelligence

**Hooks Learn Across Projects**:
```bash
# Working on Project A (React app)
# → Hooks learn your React patterns and preferences
# → Decisions about state management stored automatically

# Switch to Project B (React app)  
# → Hooks detect similar project type
# → Automatically inject relevant React knowledge from Project A
# → "You previously chose Redux for state management because..."
```

#### Team Collaboration with Hooks

**Individual + Team Memory**:
```bash
# Your personal hooks capture individual work patterns
# Team uses shared memory service for collaborative decisions
# Result: Personal context + team knowledge in every session

# Example auto-injected context:
# "Personal: You prefer TypeScript for type safety
#  Team: Architecture meeting decided on microservices approach  
#  Project: Authentication module 90% complete"
```

#### Automatic Learning Progression

**Hooks Build Knowledge Over Time**:
```bash
# Month 1: Basic project setup decisions stored
# Month 2: Hooks identify patterns, inject relevant past learnings
# Month 3: Hooks provide increasingly sophisticated context
# Month 6: Claude Code becomes project-specific expert assistant

# Example progression:
# Week 1: "Starting new React project"
# Week 4: "Based on your React patterns, consider using..."  
# Month 3: "Your established architecture suggests..."
# Month 6: "Consistent with your advanced React practices..."
```

---

## Commands vs MCP Server vs Hooks

### When to Choose Commands

**✅ Perfect For**:
- Individual developers who want manual control
- Quick setup (2 minutes to working)
- Direct command-line interface preference
- Explicit memory operations
- Zero configuration requirements

**✅ Benefits**:
- Immediate access to memory operations
- Built-in help and guidance
- Context-aware project detection
- Auto-discovery of memory service
- Professional conversational interface
- **Manual control** - you decide when to store/retrieve

**❌ Limitations**:
- Requires explicit user action for every operation
- No automatic session continuity
- Manual memory injection needed

### When to Choose MCP Server

**✅ Perfect For**:
- Team environments with shared memory service
- Complex multi-server MCP workflows
- Integration with other MCP tools
- Maximum configuration flexibility
- Traditional MCP tool interactions

**✅ Benefits**:
- Full MCP protocol compliance
- Works alongside other MCP servers
- Conversational natural language interface
- Advanced server configuration options
- Standard MCP debugging and monitoring

**❌ Limitations**:
- Requires MCP server configuration
- No automatic session lifecycle management
- Manual memory operations through MCP protocol

### When to Choose Memory Awareness Hooks

**✅ Perfect For**:
- Developers who want seamless, automatic memory integration
- Long-term project continuity across sessions
- Zero-effort memory management
- Automatic context preservation
- Transparent background operation

**✅ Benefits**:
- **Fully automatic** - zero manual intervention required
- **Session continuity** - every session builds on previous work
- **Intelligent context** - automatic project-aware memory injection
- **Background consolidation** - outcomes stored automatically
- **Cross-session learning** - Claude Code gets smarter over time
- **Perfect memory** - never lose important decisions or insights

**❌ Limitations**:
- Requires Node.js for hook execution
- Less manual control over memory operations
- Background processing may add slight startup delay

### Comparison Matrix

| Feature | Commands | MCP Server | **Memory Hooks** |
|---------|----------|------------|------------------|
| **Setup Complexity** | Minimal | Medium | Minimal |
| **Manual Control** | High | High | **Low** |
| **Automatic Operation** | None | None | **Complete** |
| **Session Continuity** | None | None | **Perfect** |
| **Project Awareness** | Manual | Manual | **Automatic** |
| **Context Injection** | Manual | Manual | **Automatic** |
| **Memory Consolidation** | Manual | Manual | **Automatic** |
| **Learning Over Time** | No | No | **Yes** |
| **Background Processing** | No | No | **Yes** |
| **User Intervention** | Required | Required | **Optional** |

### Recommended Approach: **Hybrid Usage**

**🎯 Optimal Setup**: Use **Memory Hooks + Commands** together

```bash
# Install both systems
python install.py --install-claude-commands --install-claude-hooks

# Result:
# ✅ Automatic session continuity (hooks)  
# ✅ Manual control when needed (commands)
# ✅ Best of both worlds
```

**How They Work Together**:
1. **Hooks handle automatic background work**: Session startup, consolidation, context injection
2. **Commands handle explicit operations**: Specific searches, manual storage, health checks
3. **No conflicts**: They use the same memory service and enhance each other

**Example Workflow**:
```bash
# Hooks automatically inject context when Claude Code starts
# → You have full project history without doing anything

# During development, use commands for specific needs:
claude /memory-store "Important architectural decision about microservices"
claude /memory-search --tags "database,performance" 

# Hooks automatically consolidate session when Claude Code ends
# → Your insights are preserved for next time
```

### Can I Use All Three?
**✅ Yes!** Commands, MCP Server, and Hooks are fully compatible:
- Same underlying memory service and database
- Switch between methods as needed
- Each approach serves different use cases
- No conflicts or data compatibility issues

See the complete [Commands vs MCP Server Guide](../guides/commands-vs-mcp-server.md) for detailed comparison.

---

## Troubleshooting

### Commands Not Working

**Issue**: Commands not found or not executing
```bash
# Check Claude Code CLI
claude --version  # Should show version info

# Check if commands are installed
ls ~/.claude/commands/memory-*.md

# Reinstall commands
python scripts/claude_commands_utils.py

# Test installation prerequisites
python scripts/claude_commands_utils.py --test
```

### Memory Service Connection Issues

**Issue**: Commands can't connect to memory service
```bash
# Check if memory service is running
memory --help

# Test service health
claude /memory-health

# Start memory service manually
memory  # Starts interactive service

# Check service auto-discovery
# Commands use mDNS to find running services automatically
```

### Permission Issues

**Issue**: Cannot install or access commands
```bash
# Check commands directory permissions
ls -la ~/.claude/commands/

# Ensure write access to commands directory
chmod 755 ~/.claude/commands/

# Try installation with explicit permissions
sudo python scripts/claude_commands_utils.py  # Not recommended, troubleshoot first
```

### Performance Issues

**Issue**: Commands are slow or unresponsive
```bash
# Check service health and performance
claude /memory-health --detailed --performance-test

# Check memory service resources
# Commands automatically discover and connect to optimal endpoints

# Clear any cached data
claude /memory-health --fix-issues
```

### Installation Issues

**Issue**: Installation fails or incomplete
```bash
# Check prerequisites
python --version  # Should be 3.10+
claude --version  # Should show Claude Code version

# Clean installation
python scripts/claude_commands_utils.py --uninstall
python install.py --install-claude-commands

# Manual installation
cp claude_commands/*.md ~/.claude/commands/
```

### Memory Awareness Hooks Issues

#### Hooks Not Executing

**Issue**: No automatic memory injection during Claude Code sessions
```bash
# Verify hooks installation
ls ~/.claude-code/hooks/core/session-*.js

# Test project detection manually
cd ~/.claude-code/hooks
node utilities/project-detector.js

# Check Claude Code can find hooks
export CLAUDE_HOOKS_DEBUG=true
claude  # Start with debug output

# Verify memory service connectivity
curl -k https://your-service:8443/api/health
```

#### Session Context Not Persisting  

**Issue**: Each Claude Code session starts fresh, no memory injection
```bash
# Check session-start hook is enabled
grep -A 5 "sessionStart" ~/.claude-code/hooks/config.json

# Test memory service has data
curl -k "https://your-service:8443/api/memories/search?tags=claude-code"

# Verify hook execution timing
export CLAUDE_HOOKS_TIMING=true
claude  # Check startup timing logs
```

#### Session Outcomes Not Being Stored

**Issue**: Session-end hook not consolidating conversations
```bash
# Check session-end hook is enabled  
grep -A 5 "sessionEnd" ~/.claude-code/hooks/config.json

# Test session analysis manually
cd ~/.claude-code/hooks
node -e "
const { analyzeSession } = require('./utilities/conversation-analyzer');
console.log('Session analyzer available:', typeof analyzeSession);
"

# Verify minimum session length requirements
# Edit config.json: "minSessionLength": 10  # Lower threshold for testing
```

### Getting Help

- 📖 [Full Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/doobidoo/mcp-memory-service/issues)
- 💬 [Discussions](https://github.com/doobidoo/mcp-memory-service/discussions)
- 🔍 [Search Existing Issues](https://github.com/doobidoo/mcp-memory-service/issues?q=is%3Aissue)
- 🔧 [Hooks Troubleshooting Guide](../guides/hooks-troubleshooting.md)

---

## Advanced Features

### Context-Aware Operations

Commands automatically detect and use:
- **Current Project**: Working directory and git repository information
- **Session Context**: Current conversation topics and development focus  
- **File Context**: Recent file changes and modifications
- **Temporal Context**: Time-based relevance and recency

### Smart Tagging

Automatic tag generation based on:
- Project directory name and structure
- Programming languages detected in current directory
- File types and patterns (`.js`, `.py`, `.md`, etc.)
- Git repository name and branch information
- Development context and session topics

### Service Auto-Discovery

Commands use multiple methods to find your memory service:
1. **mDNS Discovery**: Automatic service discovery on local network
2. **Default Endpoints**: Localhost ports and standard configurations
3. **Environment Variables**: Custom endpoint configuration
4. **Fallback Methods**: Graceful degradation when service unavailable

### Professional Features

- **Health Monitoring**: Comprehensive service diagnostics
- **Performance Testing**: Benchmark and optimization tools
- **Backup Verification**: Automatic backup system checking
- **Error Recovery**: Intelligent error handling and recovery suggestions
- **Export Capabilities**: Save reports and search results to files

### Integration with MCP Memory Service Features

Commands provide full access to:
- **Semantic Search**: Using sentence transformers and embeddings
- **Time-based Recall**: Natural language time expression parsing
- **Tag Management**: Flexible tagging and organization system
- **Multiple Storage Backends**: ChromaDB, SQLite-vec, and Cloudflare support
- **Cross-platform Compatibility**: Windows, macOS, and Linux support

### Memory Awareness Hooks Advanced Features

#### Intelligent Memory Selection Algorithms

**Multi-Factor Relevance Scoring**:
```javascript
relevanceScore = (
  timeDecay * 0.3 +           // Recent memories weighted higher
  tagRelevance * 0.4 +        // Project tags match current context  
  contentRelevance * 0.2 +    // Semantic similarity to current work
  typeBonus * 0.1             // Memory type relevance (decisions > notes)
)
```

**Adaptive Time Decay**:
- Recent memories (< 1 week): Full relevance score
- Medium age (1 week - 1 month): 70% relevance  
- Older memories (> 1 month): 30% relevance, but never fully discarded
- Critical decisions: Never decay below 50% relevance

#### Session Analysis and Consolidation

**Natural Language Processing Pipeline**:
1. **Topic Extraction**: Identifies main conversation themes
2. **Decision Detection**: Finds architectural and implementation decisions
3. **Insight Mining**: Extracts learning outcomes and discoveries  
4. **Next Steps Identification**: Captures action items and follow-up tasks
5. **Code Change Analysis**: Links discussions to actual code modifications

**Auto-Generated Memory Examples**:
```json
{
  "content": "Implemented OAuth2 authentication using Auth0. Chose JWT tokens over sessions for stateless API design. Next: Configure production environment variables.",
  "auto_tags": ["oauth2", "auth0", "jwt", "authentication", "api-design", "session-outcome"],
  "extracted_data": {
    "decisions": ["OAuth2 with Auth0", "JWT over sessions", "stateless API"],
    "technologies": ["Auth0", "JWT", "OAuth2"],
    "next_steps": ["configure production env vars"],
    "session_type": "implementation",
    "confidence": 0.89
  }
}
```

#### Cross-Project Pattern Recognition

**Framework Detection and Learning**:
- Recognizes when you start similar project types
- Injects relevant patterns from previous projects
- Learns your personal preferences and coding styles
- Builds project-type-specific knowledge bases

**Example Cross-Project Intelligence**:
```bash
# Previously worked on React App A: chose Redux + TypeScript
# Starting React App B: Hook automatically injects:
# "Based on your React experience: You consistently choose Redux for state management and TypeScript for type safety. Previous performance optimizations included..."
```

#### Professional Development Features

**Knowledge Graph Building**:
- Links related memories across different projects
- Identifies recurring themes and decision patterns
- Builds personal development methodology over time
- Creates searchable knowledge base of your expertise

**Competency Tracking**:
```json
{
  "technologies": {
    "React": {"experience_level": "advanced", "last_used": "2024-08-23", "key_patterns": ["hooks", "context", "performance"]},
    "Python": {"experience_level": "expert", "last_used": "2024-08-23", "key_patterns": ["fastapi", "async", "testing"]},
    "Docker": {"experience_level": "intermediate", "last_used": "2024-08-20", "learning_areas": ["multi-stage builds"]}
  }
}
```

#### Team Synchronization (Enterprise Feature)

**Shared Knowledge Integration**:
- Personal hooks work alongside team memory service
- Separates individual patterns from team decisions
- Provides context about both personal preferences and team standards
- Maintains privacy while enabling collaboration

**Example Team + Personal Context**:
```markdown
# Personal Development Context
- You prefer functional programming patterns
- Your testing approach emphasizes integration tests
- You typically choose PostgreSQL for relational data

# Team Architecture Context  
- Team standard: microservices with Docker containers
- Agreed database: MongoDB for this project
- Testing strategy: TDD with 80% coverage requirement

# Project-Specific Context
- Authentication service 90% complete
- User service next priority  
- Performance requirements: <200ms API response time
```

---

## Developer Information

### Command Architecture

Commands are implemented as:
- **Markdown Files**: Conversational interfaces in `~/.claude/commands/`
- **Python Utilities**: Installation and management in `scripts/claude_commands_utils.py`
- **Integration Logic**: Seamless installation via main `install.py`
- **Cross-platform Support**: Windows, macOS, and Linux compatibility

### Contributing

- Commands follow the CCPlugins conversational pattern
- Each command is a markdown file with structured sections
- Installation utilities provide comprehensive error handling
- Integration testing ensures cross-platform compatibility

### Customization

- Command behavior can be modified by editing markdown files
- Installation options can be customized via CLI arguments
- Service discovery can be configured via environment variables
- Advanced users can extend commands with custom functionality

---

**Enjoy your enhanced Claude Code experience with persistent memory capabilities!** 🎉