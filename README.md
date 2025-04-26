uses Cloudflare D1** for storage (serverless SQLite)
- Uses **Workers AI** for embeddings generation
- Communicates via **Server-Sent Events (SSE)** for MCP protocol
- Requires no local installation or dependencies
- Scales automatically with usage

### Benefits of the Cloudflare Implementation

- **Zero local installation**: No Python, dependencies, or local storage needed
- **Cross-platform compatibility**: Works on any device that can connect to the internet
- **Automatic scaling**: Handles multiple users without configuration
- **Global distribution**: Low latency access from anywhere
- **No maintenance**: Updates and maintenance handled automatically

### Available Tools in the Cloudflare Implementation

The Cloudflare Worker implementation supports all the same tools as the Python implementation:

| Tool | Description |
|------|-------------|
| `store_memory` | Store new information with optional tags |
| `retrieve_memory` | Find relevant memories based on query |
| `recall_memory` | Retrieve memories using natural language time expressions |
| `search_by_tag` | Search memories by tags |
| `delete_memory` | Delete a specific memory by its hash |
| `delete_by_tag` | Delete all memories with a specific tag |
| `cleanup_duplicates` | Find and remove duplicate entries |
| `get_embedding` | Get raw embedding vector for content |
| `check_embedding_model` | Check if embedding model is loaded and working |
| `debug_retrieve` | Retrieve memories with debug information |
| `exact_match_retrieve` | Retrieve memories using exact content match |
| `check_database_health` | Check database health and get statistics |
| `recall_by_timeframe` | Retrieve memories within a specific timeframe |
| `delete_by_timeframe` | Delete memories within a specific timeframe |
| `delete_before_date` | Delete memories before a specific date |

### Configuring Claude to Use the Cloudflare Memory Service

Add the following to your Claude configuration to use the Cloudflare-based memory service:

```json
{
  "mcpServers": [
    {
      "name": "cloudflare-memory",
      "url": "https://your-worker-subdomain.workers.dev/mcp",
      "type": "sse"
    }
  ]
}
```

Replace `your-worker-subdomain` with your actual Cloudflare Worker subdomain.

### Deploying Your Own Cloudflare Memory Service

1. Clone the repository and navigate to the Cloudflare Worker directory:
   ```bash
   git clone https://github.com/doobidoo/mcp-memory-service.git
   cd mcp-memory-service/cloudflare_worker
   ```

2. Install Wrangler (Cloudflare's CLI tool):
   ```bash
   npm install -g wrangler
   ```

3. Login to your Cloudflare account:
   ```bash
   wrangler login
   ```

4. Create a D1 database:
   ```bash
   wrangler d1 create mcp_memory_service
   ```

5. Update the `wrangler.toml` file with your database ID from the previous step.

6. Initialize the database schema:
   ```bash
   wrangler d1 execute mcp_memory_service --local --file=./schema.sql
   ```

   Where `schema.sql` contains:
   ```sql
   CREATE TABLE IF NOT EXISTS memories (
     id TEXT PRIMARY KEY,
     content TEXT NOT NULL,
     embedding TEXT NOT NULL,
     tags TEXT,
     memory_type TEXT,
     metadata TEXT,
     created_at INTEGER
   );
   CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at);
   ```

7. Deploy the worker:
   ```bash
   wrangler deploy
   ```

8. Update your Claude configuration to use your new worker URL.

### Testing Your Cloudflare Memory Service

After deployment, you can test your memory service using curl:

1. List available tools:
   ```bash
   curl https://your-worker-subdomain.workers.dev/list_tools
   ```

2. Store a memory:
   ```bash
   curl -X POST https://your-worker-subdomain.workers.dev/mcp \
     -H "Content-Type: application/json" \
     -d '{"method":"store_memory","arguments":{"content":"This is a test memory","metadata":{"tags":["test"]}}}'
   ```

3. Retrieve memories:
   ```bash
   curl -X POST https://your-worker-subdomain.workers.dev/mcp \
     -H "Content-Type: application/json" \
     -d '{"method":"retrieve_memory","arguments":{"query":"test memory","n_results":5}}'
   ```

### Limitations

- Free tier limits on Cloudflare Workers and D1 may apply
- Workers AI embedding models may differ slightly from the local sentence-transformers models
- No direct access to the underlying database for manual operations
- Cloudflare Workers have a maximum execution time of 30 seconds on free plans