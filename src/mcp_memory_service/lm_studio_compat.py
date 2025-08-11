"""
LM Studio compatibility patch for MCP Memory Service.

This module provides a monkey patch to handle LM Studio's non-standard
'notifications/cancelled' message that isn't part of the standard MCP protocol.
"""

import logging
import sys
import platform
from typing import Any, Dict, Union
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

def add_windows_timeout_handling():
    """
    Add Windows-specific timeout and error handling.
    """
    if platform.system() != "Windows":
        return
    
    try:
        # Add better timeout handling for Windows
        import signal
        import asyncio
        
        def timeout_handler(signum, frame):
            logger.warning("Server received timeout signal - attempting graceful shutdown")
            print("Server timeout detected - shutting down gracefully", file=sys.stderr, flush=True)
            sys.exit(0)
        
        # Only set up signal handlers if they're available
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, timeout_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, timeout_handler)
            
        logger.info("Added Windows-specific timeout handling")
        
    except Exception as e:
        logger.debug(f"Could not set up Windows timeout handling: {e}")
        # Not critical, continue without it

def patch_mcp_for_lm_studio():
    """
    Apply monkey patches to MCP library to handle LM Studio's non-standard notifications.
    """
    try:
        # Import the MCP shared session module
        import mcp.shared.session as session_module
        
        # Store the original _receive_notification_type if it exists
        if hasattr(session_module, 'ClientNotification'):
            original_client_notification = session_module.ClientNotification
            
            # Create a wrapper that handles the cancelled notification
            class PatchedClientNotification:
                @classmethod
                def model_validate(cls, obj, *args, **kwargs):
                    """
                    Patched validation that handles LM Studio's cancelled notification.
                    """
                    # Check if this is a cancelled notification from LM Studio or Claude Desktop
                    if isinstance(obj, dict):
                        method = obj.get('method', '')
                        if method == 'notifications/cancelled':
                            params = obj.get('params', {})
                            reason = params.get('reason', 'Unknown reason')
                            request_id = params.get('requestId', 'unknown')
                            
                            logger.info(f"Intercepted cancelled notification (ID: {request_id}): {reason}")
                            
                            # Check if this is a timeout - handle gracefully
                            if 'timed out' in reason.lower() or 'timeout' in reason.lower():
                                logger.warning(f"Operation timeout detected: {reason}")
                                # Don't exit on timeout - just log and continue
                            
                            # Return a mock notification that won't cause validation errors
                            # Use a proper Pydantic model structure
                            try:
                                from mcp.types import InitializedNotification
                                # Create a valid initialized notification instead
                                return InitializedNotification()
                            except ImportError:
                                # Fallback to a simple mock object
                                return type('MockNotification', (), {
                                    'method': 'notifications/initialized',
                                    'params': {}
                                })()
                    
                    # Use the original validation for all other cases
                    return original_client_notification.model_validate(obj, *args, **kwargs)
                
                def __getattr__(self, name):
                    # Forward all other attributes to the original class
                    return getattr(original_client_notification, name)
            
            # Replace the ClientNotification in the module
            session_module.ClientNotification = PatchedClientNotification
            
            logger.info("Applied enhanced LM Studio/Claude Desktop compatibility patch for notifications/cancelled")
            return True
        else:
            logger.warning("Could not find ClientNotification to patch")
            return False
        
    except ImportError as e:
        logger.warning(f"Could not import MCP session module: {e}")
        # Try alternative patching approach
        return patch_alternative_approach()
    except Exception as e:
        logger.error(f"Error applying LM Studio compatibility patch: {e}")
        return False


def patch_alternative_approach():
    """
    Alternative patching approach that modifies the session's receive loop.
    """
    try:
        import mcp.shared.session
        import asyncio
        
        # Get the Session class
        Session = mcp.shared.session.Session
        
        # Store the original _receive_loop method
        if hasattr(Session, '_receive_loop'):
            original_receive_loop = Session._receive_loop
            
            async def patched_receive_loop(self):
                """Patched receive loop that handles cancelled notifications and timeouts gracefully."""
                try:
                    await original_receive_loop(self)
                except Exception as e:
                    error_str = str(e)
                    # Check if this is the specific LM Studio/Claude Desktop cancelled notification error
                    if 'notifications/cancelled' in error_str:
                        if 'timed out' in error_str.lower() or 'timeout' in error_str.lower():
                            logger.warning("Operation timeout in receive loop - continuing gracefully")
                        else:
                            logger.debug("Ignoring cancelled notification error in receive loop")
                        # Don't recursively call - just return to allow graceful exit
                        return
                    elif 'ValidationError' in error_str and 'notifications/cancelled' in error_str:
                        logger.warning("Validation error for cancelled notification - continuing gracefully") 
                        return
                    else:
                        # Re-raise other errors
                        raise
            
            # Apply the patch
            Session._receive_loop = patched_receive_loop
            logger.info("Applied alternative LM Studio/Claude Desktop compatibility patch")
            return True
        else:
            logger.warning("Could not find _receive_loop to patch")
            return False
            
    except Exception as e:
        logger.error(f"Error in alternative patch approach: {e}")
        return False