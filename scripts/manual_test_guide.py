#!/usr/bin/env python3
"""
Manual testing guide with curl commands and examples.
"""

def print_manual_test_guide():
    print("""
🎯 MCP Memory Service - Manual Testing Guide
============================================

Prerequisites:
1. Start the server: python scripts/run_http_server.py
2. Server should be running on http://localhost:8000

🔍 BASIC HEALTH CHECKS
----------------------
curl http://localhost:8000/api/health
curl http://localhost:8000/api/health/detailed

💾 MEMORY OPERATIONS
--------------------
# Store a memory
curl -X POST http://localhost:8000/api/memories \\
  -H "Content-Type: application/json" \\
  -d '{
    "content": "Test memory for manual testing",
    "tags": ["test", "manual"],
    "memory_type": "test",
    "metadata": {"source": "manual_test"}
  }'

# List memories
curl "http://localhost:8000/api/memories?page=1&page_size=5"

# List memories with tag filter
curl "http://localhost:8000/api/memories?tag=test"

# Delete a memory (replace HASH with actual content_hash from store response)
curl -X DELETE http://localhost:8000/api/memories/HASH

🔍 SEARCH OPERATIONS
--------------------
# Semantic search
curl -X POST http://localhost:8000/api/search \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "test memory",
    "n_results": 5,
    "similarity_threshold": 0.1
  }'

# Tag-based search
curl -X POST http://localhost:8000/api/search/by-tag \\
  -H "Content-Type: application/json" \\
  -d '{
    "tags": ["test"],
    "match_all": false
  }'

# Time-based search
curl -X POST http://localhost:8000/api/search/by-time \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "today",
    "n_results": 10
  }'

📡 SSE TESTING
--------------
# Connect to SSE stream (in browser or with curl)
curl -N http://localhost:8000/api/events

# Get SSE connection stats
curl http://localhost:8000/api/events/stats

🌐 BROWSER TESTING
------------------
Open these URLs in your browser:

1. Main Dashboard:
   http://localhost:8000

2. API Documentation (Swagger):
   http://localhost:8000/api/docs

3. Real-time SSE Demo:
   http://localhost:8000/static/sse_test.html

4. Interactive API Testing:
   http://localhost:8000/api/redoc

📊 PERFORMANCE TESTING
----------------------
# Test with multiple concurrent requests
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/memories \\
    -H "Content-Type: application/json" \\
    -d "{\"content\": \"Concurrent test $i\", \"tags\": [\"concurrent\"]}" &
done
wait

🔧 TROUBLESHOOTING
------------------
If tests fail:

1. Check server logs for errors
2. Verify all dependencies are installed:
   pip install fastapi uvicorn sse-starlette aiofiles psutil sqlite-vec sentence-transformers

3. Check if ports are available:
   netstat -an | grep :8000

4. Test individual components:
   python -c "from mcp_memory_service.web.app import app; print('Import successful')"

🎉 SUCCESS INDICATORS
---------------------
✅ Health endpoint returns {"status": "healthy"}
✅ Memory operations return success: true
✅ Search operations return results with processing times
✅ SSE stream shows heartbeat events every 30 seconds
✅ Browser demo shows real-time events when operations are performed

""")

if __name__ == "__main__":
    print_manual_test_guide()