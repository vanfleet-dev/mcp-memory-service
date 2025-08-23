# Memory Awareness Hooks - Detailed Guide

This is the comprehensive guide for Claude Code Memory Awareness Hooks, providing detailed installation, configuration, troubleshooting, and architecture information.

## Table of Contents
- [Architecture](#architecture)
- [Installation Methods](#installation-methods)
- [Configuration Details](#configuration-details)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [Development](#development)

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
- `config.template.json` - Configuration template with defaults

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

## Installation Methods

### Automated Installation (Recommended)

The automated installer handles the complete setup:

```bash
cd claude-hooks
./install.sh
```

**What the installer does:**
1. Creates `~/.claude/hooks/` directory
2. Copies all hook files to correct location
3. Configures `~/.claude/settings.json` with hook integration
4. Backs up existing configuration
5. Runs comprehensive integration tests (14 tests)
6. Tests memory service connectivity
7. Provides detailed installation report

**Installation Options:**
```bash
./install.sh              # Full installation
./install.sh --help       # Show help
./install.sh --uninstall  # Remove hooks
./install.sh --test       # Run tests only
```

### Manual Installation (Advanced Users)

For users who prefer manual control or need custom configurations:

1. **Copy Hook Files**:
```bash
# Create directory structure
mkdir -p ~/.claude/hooks/{core,utilities,tests}

# Copy files
cp claude-hooks/core/*.js ~/.claude/hooks/core/
cp claude-hooks/utilities/*.js ~/.claude/hooks/utilities/
cp claude-hooks/tests/*.js ~/.claude/hooks/tests/
cp claude-hooks/config.* ~/.claude/hooks/
cp claude-hooks/README.md ~/.claude/hooks/
```

2. **Configure Claude Code Settings**:
```bash
# Create or edit ~/.claude/settings.json
cat > ~/.claude/settings.json << 'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node ~/.claude/hooks/core/session-start.js",
            "timeout": 10
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node ~/.claude/hooks/core/session-end.js",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
EOF
```

3. **Configure Memory Service**:
```bash
cd ~/.claude/hooks
cp config.template.json config.json
# Edit config.json with your settings
```

4. **Test Installation**:
```bash
cd ~/.claude/hooks
node tests/integration-test.js
```

## Configuration Details

### Memory Service Configuration

Edit `~/.claude/hooks/config.json`:

```json
{
  "memoryService": {
    "endpoint": "https://your-server:8443",
    "apiKey": "your-api-key",
    "defaultTags": ["claude-code", "auto-generated"],
    "maxMemoriesPerSession": 10
  },
  "projectDetection": {
    "gitRepository": true,
    "packageFiles": ["package.json", "pyproject.toml", "Cargo.toml"],
    "frameworkDetection": true,
    "languageDetection": true
  },
  "sessionAnalysis": {
    "extractTopics": true,
    "extractDecisions": true,
    "extractInsights": true,
    "extractCodeChanges": true,
    "extractNextSteps": true,
    "minSessionLength": 100
  }
}
```

### Project Detection Rules

The system detects projects based on:

- **Git Repository**: Checks for `.git` directory
- **Package Files**: Looks for `package.json`, `pyproject.toml`, `Cargo.toml`, etc.
- **Framework Detection**: Identifies React, Vue, Django, etc.
- **Language Detection**: Analyzes file extensions and content

### Memory Filtering

Configure memory selection preferences:

```json
{
  "memoryFilters": {
    "timeDecay": {
      "enabled": true,
      "decayFactor": 0.95,
      "maxAge": "30d"
    },
    "relevanceThreshold": 0.3,
    "excludeTags": ["temporary", "draft"],
    "priorityTags": ["architecture", "decision", "bug-fix"]
  }
}
```

### Advanced Settings

```json
{
  "hooks": {
    "sessionStart": {
      "enabled": true,
      "timeout": 10,
      "retries": 2,
      "verboseLogging": false
    },
    "sessionEnd": {
      "enabled": true,
      "timeout": 15,
      "consolidationEnabled": true,
      "autoTagging": true
    }
  },
  "performance": {
    "cacheMemories": true,
    "cacheDuration": "1h",
    "maxConcurrentRequests": 3
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Hooks Not Detected
**Problem**: Claude Code shows "Found 0 hook matchers in settings"

**Diagnosis**:
```bash
# Check settings file exists and is valid
ls ~/.claude/settings.json
cat ~/.claude/settings.json | jq .hooks

# Verify hook files exist
ls -la ~/.claude/hooks/core/
```

**Solutions**:
1. **Reinstall hooks**: `cd claude-hooks && ./install.sh`
2. **Check settings format**: Settings must be valid JSON with proper structure
3. **Verify file permissions**: `chmod +x ~/.claude/hooks/core/*.js`
4. **Test Claude Code**: `claude --debug hooks`

#### 2. JSON Parsing Errors  
**Problem**: "Parse error: Expected property name or '}' in JSON"

**Cause**: Memory service returns Python dictionary format with single quotes

**Solutions**:
1. **Update to latest version**: The current version includes Python→JSON conversion
2. **Verify fix is applied**: Check that `session-start.js` includes string replacement logic
3. **Test parsing manually**:
```bash
node -e "
const testData = '{\"results\": [{\"content\": \"test\"}]}';
console.log(JSON.parse(testData));
"
```

#### 3. Memory Service Connection Failed
**Problem**: "Network error" or "ENOTFOUND" in hook output

**Diagnosis**:
```bash
# Test service availability
curl -k https://your-endpoint:8443/api/health

# Check configuration
cat ~/.claude/hooks/config.json | jq .memoryService

# Test network connectivity
ping your-server-hostname
```

**Solutions**:
1. **Verify service is running**: Check memory service status
2. **Update endpoint URL**: Edit `~/.claude/hooks/config.json`
3. **Check API key**: Ensure correct API key is configured
4. **Firewall/network**: Verify port 8443 is accessible
5. **SSL certificates**: Self-signed certs may need special handling

#### 4. Wrong Installation Directory
**Problem**: Hooks installed but Claude Code can't find them

**Diagnosis**:
```bash
# Check for hooks in wrong location
ls ~/.claude-code/hooks/
ls ~/.claude/hooks/
```

**Solutions**:
1. **Move to correct location**:
```bash
mkdir -p ~/.claude/hooks
mv ~/.claude-code/hooks/* ~/.claude/hooks/
```
2. **Update settings paths**: Ensure settings.json points to `~/.claude/hooks/`
3. **Reinstall**: `cd claude-hooks && ./install.sh`

#### 5. Node.js Issues
**Problem**: "node: command not found" or version conflicts

**Solutions**:
1. **Install Node.js**: Version 14 or higher required
2. **Update PATH**: Ensure Node.js is in system PATH
3. **Check version**: `node --version && npm --version`
4. **Use full path**: Edit hooks to use `/usr/bin/node` instead of `node`

#### 6. Permission Errors
**Problem**: "Permission denied" when running hooks

**Solutions**:
```bash
# Fix hook file permissions
chmod +x ~/.claude/hooks/core/*.js
chmod +x ~/.claude/hooks/tests/*.js

# Fix directory permissions
chmod 755 ~/.claude/hooks
chmod -R 644 ~/.claude/hooks/*.json
```

### Advanced Troubleshooting

#### Debug Mode
Enable verbose logging:

```bash
# Set debug environment variable
export CLAUDE_HOOKS_DEBUG=true

# Run Claude Code with debug output
claude --debug hooks

# Test individual hooks
node ~/.claude/hooks/core/session-start.js
```

#### Hook Execution Testing

Test hooks individually:

```bash
cd ~/.claude/hooks

# Test session start hook
node core/session-start.js

# Test session end hook  
node core/session-end.js

# Test project detection
node -e "
const { detectProjectContext } = require('./utilities/project-detector');
detectProjectContext('.').then(console.log);
"

# Test memory scoring
node -e "
const { scoreMemoryRelevance } = require('./utilities/memory-scorer');
const mockMemories = [{content: 'test', tags: ['test']}];
const mockProject = {name: 'test', language: 'JavaScript'};
console.log(scoreMemoryRelevance(mockMemories, mockProject));
"
```

#### Integration Test Breakdown

Run specific test categories:

```bash
cd ~/.claude/hooks

# Run all integration tests
node tests/integration-test.js

# Test specific components (modify test file to run subset)
# Tests available:
# - Project Detection
# - Memory Relevance Scoring  
# - Context Formatting
# - Session Hook Structure
# - Configuration Loading
# - File Structure Validation
# - Mock Session Execution
# - Package Dependencies
# - Claude Code Settings Validation
# - Hook Files Location Validation
# - Claude Code CLI Availability
# - Memory Service Protocol
# - Memory Service Connectivity
```

#### Log Analysis

Hook logs appear in Claude Code debug output:

```bash
# Look for these log patterns:
claude --debug hooks 2>&1 | grep -E "\[Memory Hook\]|\[Project Detector\]|\[Memory Scorer\]"

# Common log messages:
# [Memory Hook] Session starting - initializing memory awareness...
# [Memory Hook] Found X relevant memories
# [Memory Hook] Successfully injected memory context
# [Memory Hook] Session ending - consolidating outcomes...
# [Memory Hook] Parse error: [details]
# [Memory Hook] Network error: [details]
```

## Advanced Usage

### Custom Memory Filters

Create custom filtering logic by editing `memory-scorer.js`:

```javascript
// Add custom scoring factors
function calculateRelevanceScore(memory, projectContext) {
  let score = 0;
  
  // Time decay
  const ageInDays = (Date.now() - new Date(memory.created_at_iso)) / (1000 * 60 * 60 * 24);
  score += Math.exp(-ageInDays / 30) * 0.3;
  
  // Tag matching
  const projectTags = [projectContext.name, projectContext.language];
  const tagMatches = memory.tags.filter(tag => projectTags.includes(tag)).length;
  score += tagMatches * 0.4;
  
  // Custom business logic
  if (memory.memory_type === 'decision') score += 0.2;
  if (memory.tags.includes('critical')) score += 0.3;
  
  return Math.min(score, 1.0);
}
```

### Session Analysis Customization

Modify `session-end.js` to extract custom insights:

```javascript
// Add custom conversation analysis
function analyzeConversation(conversationData) {
  const analysis = {
    // ... existing analysis
    customInsights: [],
    businessDecisions: [],
    technicalDebts: []
  };
  
  // Extract business decisions
  const businessPatterns = [
    /decided.*business/gi,
    /business.*decision/gi,
    /strategic.*choice/gi
  ];
  
  // Extract technical debt mentions
  const techDebtPatterns = [
    /technical.*debt/gi,
    /refactor.*needed/gi,
    /todo.*later/gi
  ];
  
  // Process messages for custom patterns
  conversationData.messages.forEach(msg => {
    businessPatterns.forEach(pattern => {
      if (pattern.test(msg.content)) {
        analysis.businessDecisions.push(extractSentence(msg.content, pattern));
      }
    });
  });
  
  return analysis;
}
```

### Multi-Project Support

Configure project-specific memory loading:

```json
{
  "projectSpecific": {
    "enabled": true,
    "projects": {
      "my-app": {
        "memoryTags": ["my-app", "react", "frontend"],
        "maxMemories": 15,
        "priorityTypes": ["architecture", "bug-fix"]
      },
      "api-service": {
        "memoryTags": ["api-service", "nodejs", "backend"],
        "maxMemories": 10,
        "priorityTypes": ["performance", "security"]
      }
    }
  }
}
```

## Development

### Hook Development

Create custom hooks by following this structure:

```javascript
/**
 * Custom Hook Template
 */
async function customHook(context) {
    try {
        console.log('[Custom Hook] Starting...');
        
        // Your custom logic here
        const result = await performCustomOperation(context);
        
        console.log('[Custom Hook] Completed successfully');
        return result;
        
    } catch (error) {
        console.error('[Custom Hook] Error:', error.message);
        // Fail gracefully
    }
}

module.exports = {
    name: 'custom-hook',
    version: '1.0.0',
    description: 'Custom hook description',
    trigger: 'custom-event',
    handler: customHook,
    config: {
        async: true,
        timeout: 10000,
        priority: 'normal'
    }
};
```

### Testing Framework

Add custom tests to `integration-test.js`:

```javascript
// Add custom test
results.test('Custom Feature Test', () => {
    // Your test logic
    const result = testCustomFeature();
    
    if (!result.success) {
        return { success: false, error: result.error };
    }
    
    console.log('  Custom feature working correctly');
    return { success: true };
});
```

### Memory Service Integration

Test memory service integration:

```javascript
// Test custom memory operations
async function testMemoryService() {
    const config = loadConfig();
    
    // Store test memory
    const storeResult = await storeMemory(config.endpoint, config.apiKey, {
        content: 'Test memory content',
        tags: ['test', 'integration'],
        memory_type: 'test'
    });
    
    // Retrieve memories
    const retrieveResult = await retrieveMemories(config.endpoint, config.apiKey, {
        query: 'test content',
        limit: 5
    });
    
    return { storeResult, retrieveResult };
}
```

### Contributing

To contribute to the hooks system:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-hook`
3. Add your hook in appropriate directory (`core/`, `utilities/`, etc.)
4. Add tests in `tests/` directory
5. Update documentation
6. Test thoroughly: `./install.sh --test`
7. Submit pull request

### Architecture Diagrams

#### Memory Injection Flow
```
Session Start → Project Detection → Memory Query → Relevance Scoring → Context Injection
     ↓                ↓                ↓               ↓               ↓
   Hook Event    Git/Package      MCP Protocol    Scoring Algorithm   Claude Context
   Triggered     File Analysis    JSON-RPC Call   Time/Tag/Content    System Message
```

#### Dynamic Updates Flow  
```
Topic Change → Semantic Analysis → Additional Memory Query → Context Update
     ↓               ↓                      ↓                   ↓
  Conversation    NLP Processing         Enhanced Query        Live Injection
  Analysis        Topic Extraction      Refined Parameters    Memory Append
```

#### Consolidation Flow
```
Session End → Conversation Analysis → Auto-Tagging → Memory Storage → Cross-Linking
     ↓               ↓                    ↓             ↓              ↓
  Hook Event    Extract Insights     Generate Tags    Store via API   Update Relations
  Triggered     Parse Decisions      ML Classification REST/MCP       Build Knowledge Graph
```

This comprehensive system transforms Claude Code into a memory-aware development assistant that maintains perfect context across all interactions, learns from every session, and provides increasingly relevant suggestions over time.