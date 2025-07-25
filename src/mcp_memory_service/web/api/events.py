"""
Server-Sent Events endpoints for real-time updates.
"""

from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from typing import Dict, Any

from ..sse import create_event_stream, sse_manager
from ..dependencies import get_storage

router = APIRouter()


class SSEStatsResponse(BaseModel):
    """Response model for SSE connection statistics."""
    total_connections: int
    heartbeat_interval: int
    connections: list


@router.get("/events")
async def events_endpoint(request: Request):
    """
    Server-Sent Events endpoint for real-time updates.
    
    Provides a continuous stream of events including:
    - memory_stored: When new memories are added
    - memory_deleted: When memories are removed
    - search_completed: When searches finish
    - health_update: System status changes
    - heartbeat: Periodic keep-alive signals
    - connection_established: Welcome message
    """
    return await create_event_stream(request)


@router.get("/events/stats", response_model=SSEStatsResponse)
async def get_sse_stats():
    """
    Get statistics about current SSE connections.
    
    Returns information about active connections, connection duration,
    and heartbeat status.
    """
    stats = sse_manager.get_connection_stats()
    return SSEStatsResponse(**stats)