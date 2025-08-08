# LM Studio Compatibility Guide

## Issue Description

When using MCP Memory Service with LM Studio, you may encounter the following error when the LM Studio client cancels an operation:

```
pydantic_core._pydantic_core.ValidationError: 5 validation errors for ClientNotification
ProgressNotification.method
  Input should be 'notifications/progress' [type=literal_error, input_value='notifications/cancelled', input_type=str]
```

This occurs because LM Studio sends a non-standard `notifications/cancelled` message that isn't part of the official MCP (Model Context Protocol) specification.

## Solution

The MCP Memory Service now includes an automatic compatibility patch that handles LM Studio's non-standard notifications. This patch is applied automatically when the server starts.

### How It Works

1. **Automatic Detection**: The server detects when LM Studio sends a `notifications/cancelled` message
2. **Graceful Handling**: Instead of crashing, the server ignores these non-standard notifications
3. **Continued Operation**: The server continues to operate normally, allowing you to use MCP tools

### What You Need to Do

**Nothing!** The compatibility patch is applied automatically when you start the MCP Memory Service.

### Verifying the Fix

You can verify the patch is working by checking the server logs. You should see:

```
Applied LM Studio compatibility patch for notifications/cancelled
```

When LM Studio cancels an operation, you'll see:

```
Intercepted LM Studio cancelled notification, ignoring it
```

Instead of a crash, the server will continue running.

## Technical Details

The compatibility layer is implemented in `src/mcp_memory_service/lm_studio_compat.py` and:

1. Monkey-patches the MCP library's `ClientNotification.model_validate` method
2. Intercepts `notifications/cancelled` messages before validation
3. Substitutes a harmless notification that won't cause errors
4. Allows normal notifications to pass through unchanged

## Limitations

- This is a workaround for LM Studio's non-standard implementation
- The cancelled notifications are ignored rather than processed
- Operations may not be properly cancelled on the server side

## Future Improvements

Ideally, this should be fixed in one of two ways:

1. **LM Studio Update**: LM Studio should follow the MCP specification and not send non-standard notifications
2. **MCP Library Update**: The MCP library could be updated to handle vendor-specific extensions gracefully

## Troubleshooting

If you still experience issues:

1. Ensure you're using the latest version of MCP Memory Service
2. Check that the patch is being applied (look for the log message)
3. Report the issue with full error logs to the repository

## Related Issues

- This is a known compatibility issue between LM Studio and the MCP protocol
- Similar issues may occur with other non-standard MCP clients
- The patch specifically handles LM Studio's behavior and may need updates for other clients