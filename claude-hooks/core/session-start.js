/**
 * Claude Code Session Start Hook
 * Automatically injects relevant memories at the beginning of each session
 */

const fs = require('fs').promises;
const path = require('path');
const https = require('https');

// Import utilities
const { detectProjectContext } = require('../utilities/project-detector');
const { scoreMemoryRelevance } = require('../utilities/memory-scorer');
const { formatMemoriesForContext } = require('../utilities/context-formatter');
const { detectContextShift, extractCurrentContext, determineRefreshStrategy } = require('../utilities/context-shift-detector');

/**
 * Load hook configuration
 */
async function loadConfig() {
    try {
        const configPath = path.join(__dirname, '../config.json');
        const configData = await fs.readFile(configPath, 'utf8');
        return JSON.parse(configData);
    } catch (error) {
        console.warn('[Memory Hook] Using default configuration:', error.message);
        return {
            memoryService: {
                endpoint: 'https://narrowbox.local:8443',
                apiKey: 'test-key-123',
                defaultTags: ['claude-code', 'auto-generated'],
                maxMemoriesPerSession: 8,
                injectAfterCompacting: false
            },
            projectDetection: {
                gitRepository: true,
                packageFiles: ['package.json', 'pyproject.toml', 'Cargo.toml'],
                frameworkDetection: true,
                languageDetection: true
            },
            output: {
                verbose: true, // Default to verbose for backward compatibility
                showMemoryDetails: false, // Hide detailed memory scoring by default
                showProjectDetails: true, // Show project detection by default
                showScoringDetails: false, // Hide detailed scoring breakdown
                cleanMode: false // Default to normal output
            }
        };
    }
}

/**
 * Query memory service for relevant memories
 */
async function queryMemoryService(endpoint, apiKey, query) {
    return new Promise((resolve, reject) => {
        const url = new URL('/mcp', endpoint);
        const postData = JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'tools/call',
            params: {
                name: 'retrieve_memory',
                arguments: {
                    query: query.semanticQuery || '',
                    n_results: query.limit || 10
                }
            }
        });

        const options = {
            hostname: url.hostname,
            port: url.port || 8443,
            path: url.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData),
                'Authorization': `Bearer ${apiKey}`
            },
            rejectUnauthorized: false // For self-signed certificates
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                try {
                    const response = JSON.parse(data);
                    if (response.result && response.result.content) {
                        // The response.result.content[0].text contains a Python dict format string
                        let textData = response.result.content[0].text;
                        
                        try {
                            // Convert Python dict format to JSON format safely
                            textData = textData
                                .replace(/'/g, '"')  // Replace single quotes with double quotes
                                .replace(/True/g, 'true')  // Convert Python True to JSON true
                                .replace(/False/g, 'false')  // Convert Python False to JSON false
                                .replace(/None/g, 'null');  // Convert Python None to JSON null
                            
                            const memories = JSON.parse(textData);
                            resolve(memories.results || memories.memories || []);
                        } catch (conversionError) {
                            console.warn('[Memory Hook] Could not parse memory response:', conversionError.message);
                            console.warn('[Memory Hook] Raw text preview:', textData.substring(0, 200) + '...');
                            resolve([]);
                        }
                    } else {
                        resolve([]);
                    }
                } catch (parseError) {
                    console.warn('[Memory Hook] Parse error:', parseError.message);
                    resolve([]);
                }
            });
        });

        req.on('error', (error) => {
            console.warn('[Memory Hook] Network error:', error.message);
            resolve([]);
        });

        req.write(postData);
        req.end();
    });
}

// ANSI Colors for console output
const CONSOLE_COLORS = {
    RESET: '\x1b[0m',
    BRIGHT: '\x1b[1m',
    DIM: '\x1b[2m',
    CYAN: '\x1b[36m',
    GREEN: '\x1b[32m',
    BLUE: '\x1b[34m',
    YELLOW: '\x1b[33m',
    GRAY: '\x1b[90m',
    RED: '\x1b[31m'
};

/**
 * Main session start hook function with enhanced visual output
 */
async function onSessionStart(context) {
    try {
        // Load configuration first to check verbosity settings
        const config = await loadConfig();
        const verbose = config.output?.verbose !== false; // Default to true
        const cleanMode = config.output?.cleanMode === true; // Default to false
        const showMemoryDetails = config.output?.showMemoryDetails === true;
        const showProjectDetails = config.output?.showProjectDetails !== false; // Default to true
        
        if (verbose && !cleanMode) {
            console.log(`${CONSOLE_COLORS.CYAN}🧠 Memory Hook${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Initializing session awareness...`);
        }
        
        // Check if this is triggered by a compacting event and skip if configured to do so
        if (context.trigger === 'compacting' || context.event === 'memory-compacted') {
            if (!config.memoryService.injectAfterCompacting) {
                console.log(`${CONSOLE_COLORS.YELLOW}⏸️  Memory Hook${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Skipping injection after compacting`);
                return;
            }
            console.log(`${CONSOLE_COLORS.GREEN}▶️  Memory Hook${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Proceeding with injection after compacting`);
        }
        
        // For non-session-start events, use smart timing to decide if refresh is needed
        if (context.trigger !== 'session-start' && context.trigger !== 'start') {
            const currentContext = extractCurrentContext(context.conversationState || {}, context.workingDirectory);
            const previousContext = context.previousContext || context.conversationState?.previousContext;
            
            if (previousContext) {
                const shiftDetection = detectContextShift(currentContext, previousContext);
                
                if (!shiftDetection.shouldRefresh) {
                    console.log(`${CONSOLE_COLORS.GRAY}⏸️  Memory Hook${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.GRAY}No context shift detected, skipping${CONSOLE_COLORS.RESET}`);
                    return;
                }
                
                console.log(`${CONSOLE_COLORS.BLUE}🔄 Memory Hook${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Context shift: ${shiftDetection.description}`);
            }
        }
        
        // Detect project context
        const projectContext = await detectProjectContext(context.workingDirectory || process.cwd());
        if (verbose && showProjectDetails && !cleanMode) {
            console.log(`${CONSOLE_COLORS.BLUE}📂 Project${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.BRIGHT}${projectContext.name}${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.GRAY}(${projectContext.language})${CONSOLE_COLORS.RESET}`);
        }
        
        // Build query for relevant memories
        const memoryQuery = {
            tags: [
                projectContext.name,
                `language:${projectContext.language}`,
                'key-decisions',
                'architecture',
                'recent-insights',
                'claude-code-reference'
            ].filter(Boolean),
            semanticQuery: context.userMessage ? 
                `${projectContext.name} ${context.userMessage}` :
                `${projectContext.name} project context decisions architecture`,
            limit: config.memoryService.maxMemoriesPerSession,
            timeFilter: 'last-2-weeks'
        };
        
        // Query memory service
        const memories = await queryMemoryService(
            config.memoryService.endpoint,
            config.memoryService.apiKey,
            memoryQuery
        );
        
        if (memories.length > 0) {
            if (verbose && showMemoryDetails && !cleanMode) {
                console.log(`${CONSOLE_COLORS.GREEN}📚 Memory Search${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Found ${CONSOLE_COLORS.BRIGHT}${memories.length}${CONSOLE_COLORS.RESET} relevant memories`);
            }
            
            // Score memories for relevance
            const scoredMemories = scoreMemoryRelevance(memories, projectContext, { verbose: showMemoryDetails });
            
            // Show top scoring memories briefly
            if (verbose && showMemoryDetails && scoredMemories.length > 0 && !cleanMode) {
                const topScores = scoredMemories.slice(0, 3).map(m => `${(m.relevanceScore * 100).toFixed(0)}%`).join(', ');
                console.log(`${CONSOLE_COLORS.CYAN}🎯 Scoring${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Top relevance: ${CONSOLE_COLORS.YELLOW}${topScores}${CONSOLE_COLORS.RESET}`);
            }
            
            // Determine refresh strategy based on context
            const strategy = context.trigger && context.previousContext ? 
                determineRefreshStrategy(detectContextShift(
                    extractCurrentContext(context.conversationState || {}, context.workingDirectory),
                    context.previousContext
                )) : {
                    maxMemories: config.memoryService.maxMemoriesPerSession,
                    includeScore: false,
                    message: '🧠 Loading relevant memory context...'
                };
            
            // Take top scored memories based on strategy
            const maxMemories = Math.min(strategy.maxMemories || config.memoryService.maxMemoriesPerSession, scoredMemories.length);
            const topMemories = scoredMemories.slice(0, maxMemories);
            
            // Show deduplication info
            if (verbose && showMemoryDetails && !cleanMode) {
                console.log(`${CONSOLE_COLORS.CYAN}🔄 Processing${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} ${maxMemories} memories selected`);
            }
            
            // Format memories for context injection with strategy-based options
            const contextMessage = formatMemoriesForContext(topMemories, projectContext, {
                includeScore: strategy.includeScore || false,
                groupByCategory: maxMemories > 3,
                maxMemories: maxMemories,
                includeTimestamp: true
            });
            
            // Inject context into session
            if (context.injectSystemMessage) {
                await context.injectSystemMessage(contextMessage);
                if (!cleanMode) {
                    console.log(`${CONSOLE_COLORS.GREEN}✅ Memory Hook${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} Context injected ${CONSOLE_COLORS.GRAY}(${maxMemories} memories)${CONSOLE_COLORS.RESET}`);
                }
            } else if (verbose && !cleanMode) {
                // Fallback: log context for manual copying with styling
                console.log(`\n${CONSOLE_COLORS.CYAN}╭──────────────────────────────────────────╮${CONSOLE_COLORS.RESET}`);
                console.log(`${CONSOLE_COLORS.CYAN}│${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.BRIGHT}Memory Context for Manual Copy${CONSOLE_COLORS.RESET}          ${CONSOLE_COLORS.CYAN}│${CONSOLE_COLORS.RESET}`);
                console.log(`${CONSOLE_COLORS.CYAN}╰──────────────────────────────────────────╯${CONSOLE_COLORS.RESET}`);
                console.log(contextMessage);
                console.log(`${CONSOLE_COLORS.CYAN}╰──────────────────────────────────────────╯${CONSOLE_COLORS.RESET}\n`);
            }
        } else if (verbose && showMemoryDetails && !cleanMode) {
            console.log(`${CONSOLE_COLORS.YELLOW}📭 Memory Search${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.GRAY}No relevant memories found${CONSOLE_COLORS.RESET}`);
        }
        
    } catch (error) {
        console.error(`${CONSOLE_COLORS.RED}❌ Memory Hook Error${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.DIM}→${CONSOLE_COLORS.RESET} ${error.message}`);
        // Fail gracefully - don't prevent session from starting
    }
}

/**
 * Hook metadata for Claude Code
 */
module.exports = {
    name: 'memory-awareness-session-start',
    version: '2.2.0',
    description: 'Automatically inject relevant memories at session start with enhanced output control',
    trigger: 'session-start',
    handler: onSessionStart,
    config: {
        async: true,
        timeout: 10000, // 10 second timeout
        priority: 'high'
    }
};

// Direct execution support for testing
if (require.main === module) {
    // Test the hook with mock context
    const mockContext = {
        workingDirectory: process.cwd(),
        sessionId: 'test-session',
        injectSystemMessage: async (message) => {
            const lines = message.split('\n');
            const maxLength = Math.min(80, Math.max(25, ...lines.map(l => l.length)));
            const border = '─'.repeat(maxLength - 2);
            
            console.log(`\n${CONSOLE_COLORS.CYAN}╭─${border}─╮${CONSOLE_COLORS.RESET}`);
            console.log(`${CONSOLE_COLORS.CYAN}│${CONSOLE_COLORS.RESET} ${CONSOLE_COLORS.BRIGHT}🧠 Injected Memory Context${CONSOLE_COLORS.RESET}${' '.repeat(maxLength - 27)} ${CONSOLE_COLORS.CYAN}│${CONSOLE_COLORS.RESET}`);
            console.log(`${CONSOLE_COLORS.CYAN}╰─${border}─╯${CONSOLE_COLORS.RESET}`);
            console.log(message);
            console.log(`${CONSOLE_COLORS.CYAN}╰─${border}─╯${CONSOLE_COLORS.RESET}`);
        }
    };
    
    onSessionStart(mockContext)
        .then(() => {
            // Test completed quietly
        })
        .catch(error => console.error(`${CONSOLE_COLORS.RED}❌ Hook test failed:${CONSOLE_COLORS.RESET} ${error.message}`));
}