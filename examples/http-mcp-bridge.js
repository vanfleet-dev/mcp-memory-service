#!/usr/bin/env node
/**
 * HTTP-to-MCP Bridge for MCP Memory Service
 * 
 * This bridge allows MCP clients (like Claude Desktop) to connect to a remote
 * MCP Memory Service HTTP server instead of running a local instance.
 * 
 * Usage in Claude Desktop config:
 * {
 *   "mcpServers": {
 *     "memory": {
 *       "command": "node",
 *       "args": ["/path/to/http-mcp-bridge.js"],
 *       "env": {
 *         "MCP_MEMORY_HTTP_ENDPOINT": "http://your-server:8000/api",
 *         "MCP_MEMORY_API_KEY": "your-api-key"
 *       }
 *     }
 *   }
 * }
 */

const http = require('http');
const https = require('https');
const { URL } = require('url');

class HTTPMCPBridge {
    constructor() {
        this.endpoint = process.env.MCP_MEMORY_HTTP_ENDPOINT || 'http://localhost:8000/api';
        this.apiKey = process.env.MCP_MEMORY_API_KEY;
        this.requestId = 0;
    }

    /**
     * Make HTTP request to the MCP Memory Service
     */
    async makeRequest(path, method = 'GET', data = null) {
        return new Promise((resolve, reject) => {
            const url = new URL(path, this.endpoint);
            const protocol = url.protocol === 'https:' ? https : http;
            
            const options = {
                hostname: url.hostname,
                port: url.port,
                path: url.pathname + url.search,
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'User-Agent': 'MCP-HTTP-Bridge/1.0'
                }
            };

            if (this.apiKey) {
                options.headers['Authorization'] = `Bearer ${this.apiKey}`;
            }

            if (data) {
                const postData = JSON.stringify(data);
                options.headers['Content-Length'] = Buffer.byteLength(postData);
            }

            const req = protocol.request(options, (res) => {
                let responseData = '';
                
                res.on('data', (chunk) => {
                    responseData += chunk;
                });
                
                res.on('end', () => {
                    try {
                        const result = JSON.parse(responseData);
                        resolve({ statusCode: res.statusCode, data: result });
                    } catch (error) {
                        reject(new Error(`Invalid JSON response: ${responseData}`));
                    }
                });
            });

            req.on('error', (error) => {
                reject(error);
            });

            if (data) {
                req.write(JSON.stringify(data));
            }
            
            req.end();
        });
    }

    /**
     * Handle MCP store_memory operation
     */
    async storeMemory(params) {
        try {
            const response = await this.makeRequest('/memories', 'POST', {
                content: params.content,
                tags: params.metadata?.tags || [],
                memory_type: params.metadata?.type || 'note',
                metadata: params.metadata || {}
            });

            if (response.statusCode === 201) {
                return { success: true, message: 'Memory stored successfully' };
            } else {
                return { success: false, message: response.data.detail || 'Failed to store memory' };
            }
        } catch (error) {
            return { success: false, message: error.message };
        }
    }

    /**
     * Handle MCP retrieve_memory operation
     */
    async retrieveMemory(params) {
        try {
            const queryParams = new URLSearchParams({
                q: params.query,
                n_results: params.n_results || 5
            });

            const response = await this.makeRequest(`/search?${queryParams}`, 'GET');

            if (response.statusCode === 200) {
                return {
                    memories: response.data.results.map(result => ({
                        content: result.memory.content,
                        metadata: {
                            tags: result.memory.tags,
                            type: result.memory.memory_type,
                            created_at: result.memory.created_at_iso,
                            relevance_score: result.relevance_score
                        }
                    }))
                };
            } else {
                return { memories: [] };
            }
        } catch (error) {
            return { memories: [] };
        }
    }

    /**
     * Handle MCP search_by_tag operation
     */
    async searchByTag(params) {
        try {
            const queryParams = new URLSearchParams();
            if (Array.isArray(params.tags)) {
                params.tags.forEach(tag => queryParams.append('tags', tag));
            } else if (typeof params.tags === 'string') {
                queryParams.append('tags', params.tags);
            }

            const response = await this.makeRequest(`/memories/search/tags?${queryParams}`, 'GET');

            if (response.statusCode === 200) {
                return {
                    memories: response.data.memories.map(memory => ({
                        content: memory.content,
                        metadata: {
                            tags: memory.tags,
                            type: memory.memory_type,
                            created_at: memory.created_at_iso
                        }
                    }))
                };
            } else {
                return { memories: [] };
            }
        } catch (error) {
            return { memories: [] };
        }
    }

    /**
     * Handle MCP delete_memory operation
     */
    async deleteMemory(params) {
        try {
            const response = await this.makeRequest(`/memories/${params.content_hash}`, 'DELETE');

            if (response.statusCode === 200) {
                return { success: true, message: 'Memory deleted successfully' };
            } else {
                return { success: false, message: response.data.detail || 'Failed to delete memory' };
            }
        } catch (error) {
            return { success: false, message: error.message };
        }
    }

    /**
     * Handle MCP check_database_health operation
     */
    async checkHealth(params = {}) {
        try {
            const response = await this.makeRequest('/health', 'GET');

            if (response.statusCode === 200) {
                return {
                    status: response.data.status,
                    backend: response.data.storage_type,
                    statistics: response.data.statistics || {}
                };
            } else {
                return { status: 'unhealthy', backend: 'unknown', statistics: {} };
            }
        } catch (error) {
            return { status: 'error', backend: 'unknown', statistics: {}, error: error.message };
        }
    }

    /**
     * Process MCP JSON-RPC request
     */
    async processRequest(request) {
        const { method, params, id } = request;

        let result;
        try {
            switch (method) {
                case 'store_memory':
                    result = await this.storeMemory(params);
                    break;
                case 'retrieve_memory':
                    result = await this.retrieveMemory(params);
                    break;
                case 'search_by_tag':
                    result = await this.searchByTag(params);
                    break;
                case 'delete_memory':
                    result = await this.deleteMemory(params);
                    break;
                case 'check_database_health':
                    result = await this.checkHealth(params);
                    break;
                default:
                    throw new Error(`Unknown method: ${method}`);
            }

            return {
                jsonrpc: "2.0",
                id: id,
                result: result
            };
        } catch (error) {
            return {
                jsonrpc: "2.0",
                id: id,
                error: {
                    code: -32000,
                    message: error.message
                }
            };
        }
    }

    /**
     * Start the bridge server
     */
    start() {
        console.error(`MCP HTTP Bridge starting...`);
        console.error(`Endpoint: ${this.endpoint}`);
        console.error(`API Key: ${this.apiKey ? '[SET]' : '[NOT SET]'}`);

        let buffer = '';

        process.stdin.on('data', async (chunk) => {
            buffer += chunk.toString();
            
            // Process complete JSON-RPC messages
            let newlineIndex;
            while ((newlineIndex = buffer.indexOf('\n')) !== -1) {
                const line = buffer.slice(0, newlineIndex).trim();
                buffer = buffer.slice(newlineIndex + 1);
                
                if (line) {
                    try {
                        const request = JSON.parse(line);
                        const response = await this.processRequest(request);
                        console.log(JSON.stringify(response));
                    } catch (error) {
                        console.error(`Error processing request: ${error.message}`);
                        console.log(JSON.stringify({
                            jsonrpc: "2.0",
                            id: null,
                            error: {
                                code: -32700,
                                message: "Parse error"
                            }
                        }));
                    }
                }
            }
        });

        process.stdin.on('end', () => {
            process.exit(0);
        });

        // Handle graceful shutdown
        process.on('SIGINT', () => {
            console.error('Shutting down HTTP Bridge...');
            process.exit(0);
        });

        process.on('SIGTERM', () => {
            console.error('Shutting down HTTP Bridge...');
            process.exit(0);
        });
    }
}

// Start the bridge if this file is run directly
if (require.main === module) {
    const bridge = new HTTPMCPBridge();
    bridge.start();
}

module.exports = HTTPMCPBridge;