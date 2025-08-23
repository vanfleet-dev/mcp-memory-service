# Claude Code Memory Awareness Hooks

This directory contains Claude Code hooks that implement automatic memory awareness and intelligent context injection for the MCP Memory Service.

## Architecture

The memory awareness system consists of three main components:

### Core Hooks
- `session-start.js` - Automatic memory injection at session initialization
- `session-end.js` - Memory consolidation and outcome storage
- `topic-change.js` - Dynamic memory loading based on conversation evolution

### Utilities
- `project-detector.js` - Project context detection and analysis
- `memory-scorer.js` - Relevance scoring algorithms for memory selection
- `context-formatter.js` - Memory formatting for Claude Code injection

### Configuration
- `config.json` - Hook configuration and memory service endpoints
- `memory-filters.json` - Memory filtering rules and preferences

## Features

### Automatic Memory Injection
- **Session Startup**: Automatically loads relevant project memories
- **Dynamic Updates**: Real-time memory injection based on conversation topics
- **Cross-Session Continuity**: Links conversations across different sessions

### Intelligent Memory Selection  
- **Project Awareness**: Detects current project and loads relevant context
- **Relevance Scoring**: AI-powered memory selection based on conversation topics
- **Time Decay**: Prioritizes recent memories while maintaining historical context

### Memory Consolidation
- **Session Outcomes**: Automatically stores conversation insights
- **Auto-Tagging**: Intelligent categorization of memory content
- **Knowledge Building**: Progressive memory organization and linking

## Installation

### Automated Installation (Recommended)

1. Run the installation script:
```bash
cd claude-hooks
./install.sh
```

The installer will automatically:
- Install hooks to the correct Claude Code directory (`~/.claude/hooks/`)
- Configure Claude Code settings for hook integration (`~/.claude/settings.json`)
- Backup any existing hooks configuration
- Run integration tests to verify installation
- Test memory service connectivity

### Manual Installation (Advanced)

1. Copy hooks to Claude Code hooks directory:
```bash
cp -r claude-hooks/* ~/.claude/hooks/
```

2. Configure Claude Code settings:
```bash
# Add to ~/.claude/settings.json
{
  "hooks": {
    "SessionStart": [{"hooks": [{"type": "command", "command": "node ~/.claude/hooks/core/session-start.js", "timeout": 10}]}],
    "SessionEnd": [{"hooks": [{"type": "command", "command": "node ~/.claude/hooks/core/session-end.js", "timeout": 15}]}]
  }
}
```

3. Configure memory service endpoint:
```bash
cd ~/.claude/hooks
cp config.template.json config.json
# Edit config.json with your memory service details
```

4. Test installation:
```bash
cd ~/.claude/hooks
node tests/integration-test.js
```

## Verification

After installation, verify hooks are working:

1. **Check Claude Code settings**:
```bash
cat ~/.claude/settings.json | grep -A10 hooks
```

2. **Test hook detection**:
```bash
claude --debug hooks  # Should show hook matchers found
```

3. **Test memory service connectivity**:
```bash
cd ~/.claude/hooks
node -e "require('./tests/integration-test').runTests()" 
```

## Configuration

### Memory Service Setup
```json
{
  "memoryService": {
    "endpoint": "https://your-server:8443",
    "apiKey": "your-api-key",
    "defaultTags": ["claude-code", "auto-generated"],
    "maxMemoriesPerSession": 10
  }
}
```

### Project Detection Rules
```json
{
  "projectDetection": {
    "gitRepository": true,
    "packageFiles": ["package.json", "pyproject.toml", "Cargo.toml"],
    "frameworkDetection": true,
    "languageDetection": true
  }
}
```

## Usage

Once installed, the hooks work automatically:

1. **Starting a Claude Code session** triggers automatic memory loading
2. **Conversation topic changes** dynamically inject additional relevant memories  
3. **Ending a session** consolidates outcomes and stores new insights

No manual intervention required - the system learns and adapts to your development patterns.

## Development

### Testing Hooks
```bash
# Test individual hooks
npm test claude-hooks/tests/session-start.test.js

# Test full workflow
npm test claude-hooks/tests/integration.test.js
```

### Debugging
Set environment variable for verbose logging:
```bash
export CLAUDE_HOOKS_DEBUG=true
claude
```

## Troubleshooting

### Common Issues

#### Hooks Not Detected
**Problem**: Claude Code shows "Found 0 hook matchers in settings"
**Solutions**:
1. Verify settings file location: `ls ~/.claude/settings.json`
2. Check settings format: `cat ~/.claude/settings.json | jq .hooks`
3. Reinstall: `cd claude-hooks && ./install.sh`

#### JSON Parsing Errors  
**Problem**: "Parse error: Expected property name or '}' in JSON"
**Cause**: Memory service returns Python dict format
**Solution**: This is fixed in the latest version. Update session-start.js:
```bash
cd ~/.claude/hooks/core
# Latest version includes Python->JSON conversion
```

#### Memory Service Connection Failed
**Problem**: "Network error" or "ENOTFOUND" in hook output
**Solutions**:
1. Verify service is running: `curl -k https://your-endpoint:8443/api/health`
2. Check endpoint in config.json: `cat ~/.claude/hooks/config.json`
3. Update API key: Edit `~/.claude/hooks/config.json`

#### Wrong Installation Directory
**Problem**: Hooks installed but Claude Code can't find them
**Solution**: 
- Old location: `~/.claude-code/hooks/` (incorrect)
- Correct location: `~/.claude/hooks/`
- Move files: `mv ~/.claude-code/hooks/* ~/.claude/hooks/`

### Verification Commands

```bash
# Check hook installation
ls -la ~/.claude/hooks/core/

# Test Claude Code hook detection
claude --debug hooks

# Test memory service
cd ~/.claude/hooks && node tests/integration-test.js

# Test individual hooks
node ~/.claude/hooks/core/session-start.js
```

### Logs and Debugging

Hook output appears in Claude Code debug mode:
```bash
claude --debug hooks
# Look for: "[Memory Hook]" messages
```

## Architecture Diagrams

### Memory Injection Flow
```
Session Start → Project Detection → Memory Query → Relevance Scoring → Context Injection
```

### Dynamic Updates Flow  
```
Topic Change → Semantic Analysis → Additional Memory Query → Context Update
```

### Consolidation Flow
```
Session End → Conversation Analysis → Auto-Tagging → Memory Storage → Cross-Linking
```

This system transforms Claude Code into a memory-aware development assistant that maintains perfect context across all interactions.