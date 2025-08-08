"""
LM Studio compatibility patch for MCP Memory Service.

This module provides a monkey patch to handle LM Studio's non-standard
'notifications/cancelled' message that isn't part of the standard MCP protocol.
"""

import logging
from typing import Any, Dict, Union
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

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
                    # Check if this is a cancelled notification from LM Studio
                    if isinstance(obj, dict):
                        method = obj.get('method', '')
                        if method == 'notifications/cancelled':
                            logger.debug(f"Intercepted LM Studio cancelled notification, ignoring it")
                            # Return None or a harmless notification that the session can handle
                            # Create a minimal valid notification structure
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
            
            logger.info("Applied LM Studio compatibility patch for notifications/cancelled")
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
        
        # Get the Session class
        Session = mcp.shared.session.Session
        
        # Store the original _receive_loop method
        if hasattr(Session, '_receive_loop'):
            original_receive_loop = Session._receive_loop
            
            async def patched_receive_loop(self):
                """Patched receive loop that ignores cancelled notifications."""
                try:
                    await original_receive_loop(self)
                except Exception as e:
                    error_str = str(e)
                    # Check if this is the specific LM Studio cancelled notification error
                    if 'notifications/cancelled' in error_str:
                        logger.debug("Ignoring LM Studio cancelled notification error in receive loop")
                        # Try to continue the loop
                        await patched_receive_loop(self)
                    else:
                        # Re-raise other errors
                        raise
            
            # Apply the patch
            Session._receive_loop = patched_receive_loop
            logger.info("Applied alternative LM Studio compatibility patch")
            return True
        else:
            logger.warning("Could not find _receive_loop to patch")
            return False
            
    except Exception as e:
        logger.error(f"Error in alternative patch approach: {e}")
        return False