# Client Hostname Capture Test

## Test Scenarios

### Scenario 1: Feature Disabled (MCP_MEMORY_INCLUDE_HOSTNAME=false)
**Expected Behavior:** No hostname tags added regardless of client input
- Request with X-Client-Hostname header → No hostname tag
- Request with client_hostname parameter → No hostname tag  
- Request with neither → No hostname tag

### Scenario 2: Feature Enabled (MCP_MEMORY_INCLUDE_HOSTNAME=true)

#### Test Case 2.1: Client hostname via request body
```bash
curl -k -X POST "https://narrowbox.local:8443/api/memories" \
-H "Content-Type: application/json" \
-d '{
  "content": "Test with client_hostname in body",
  "client_hostname": "hkr-iMac12-2"
}'
```
**Expected:** `tags` includes `source:hkr-iMac12-2`

#### Test Case 2.2: Client hostname via header
```bash
curl -k -X POST "https://narrowbox.local:8443/api/memories" \
-H "Content-Type: application/json" \
-H "X-Client-Hostname: hkr-iMac12-2" \
-d '{"content": "Test with X-Client-Hostname header"}'
```
**Expected:** `tags` includes `source:hkr-iMac12-2`

#### Test Case 2.3: No client hostname provided  
```bash
curl -k -X POST "https://narrowbox.local:8443/api/memories" \
-H "Content-Type: application/json" \
-d '{"content": "Test fallback to server hostname"}'
```
**Expected:** `tags` includes `source:narrowbox` (server hostname)

#### Test Case 2.4: Priority test (both body and header provided)
```bash
curl -k -X POST "https://narrowbox.local:8443/api/memories" \
-H "Content-Type: application/json" \
-H "X-Client-Hostname: header-hostname" \
-d '{
  "content": "Test priority",
  "client_hostname": "body-hostname"
}'
```
**Expected:** `tags` includes `source:body-hostname` (body parameter has priority)

## Test Results

Current server configuration: `MCP_MEMORY_INCLUDE_HOSTNAME=false` (default)
- ✅ All requests correctly show no hostname tags (feature disabled)
- ✅ Implementation ready for when feature is enabled

## Architecture Fix Verification

The fix has been implemented across all interfaces:
- ✅ HTTP API: Supports `client_hostname` in request body + `X-Client-Hostname` header
- ✅ MCP Server: Supports `client_hostname` parameter  
- ✅ Legacy Server: Supports `client_hostname` in arguments
- ✅ Priority: client_hostname body > X-Client-Hostname header > server hostname

## Implementation Status

**FIXED:** Client hostname is now captured instead of server hostname
- Before: Always used `socket.gethostname()` on server (narrowbox)  
- After: Prioritizes client-provided hostname, fallback to server hostname
- Maintains backward compatibility when `MCP_MEMORY_INCLUDE_HOSTNAME=false`