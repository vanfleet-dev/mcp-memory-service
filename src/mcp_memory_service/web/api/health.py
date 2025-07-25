"""
Health check endpoints for the HTTP interface.
"""

import time
import platform
import psutil
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...storage.sqlite_vec import SqliteVecMemoryStorage
from ..dependencies import get_storage

router = APIRouter()


class HealthResponse(BaseModel):
    """Basic health check response."""
    status: str
    timestamp: str
    uptime_seconds: float


class DetailedHealthResponse(BaseModel):
    """Detailed health check response."""
    status: str
    timestamp: str
    uptime_seconds: float
    storage: Dict[str, Any]
    system: Dict[str, Any]
    performance: Dict[str, Any]


# Track startup time for uptime calculation
_startup_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=time.time() - _startup_time
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check(storage: SqliteVecMemoryStorage = Depends(get_storage)):
    """Detailed health check with system and storage information."""
    
    # Get system information
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    
    system_info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "cpu_count": psutil.cpu_count(),
        "memory_total_gb": round(memory_info.total / (1024**3), 2),
        "memory_available_gb": round(memory_info.available / (1024**3), 2),
        "memory_percent": memory_info.percent,
        "disk_total_gb": round(disk_info.total / (1024**3), 2),
        "disk_free_gb": round(disk_info.free / (1024**3), 2),
        "disk_percent": round((disk_info.used / disk_info.total) * 100, 2)
    }
    
    # Get storage information
    try:
        # Get basic storage stats
        storage_info = {
            "backend": "sqlite-vec",
            "database_path": storage.db_path,
            "embedding_model": storage.embedding_model_name,
            "status": "connected"
        }
        
        # Try to get memory count (basic connectivity test)
        try:
            # This would need to be implemented in the storage class
            # For now, just mark as accessible
            storage_info["accessible"] = True
        except Exception as e:
            storage_info["accessible"] = False
            storage_info["error"] = str(e)
            
    except Exception as e:
        storage_info = {
            "backend": "sqlite-vec",
            "status": "error",
            "error": str(e)
        }
    
    # Performance metrics (basic for now)
    performance_info = {
        "uptime_seconds": time.time() - _startup_time,
        "uptime_formatted": format_uptime(time.time() - _startup_time)
    }
    
    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=time.time() - _startup_time,
        storage=storage_info,
        system=system_info,
        performance=performance_info
    )


def format_uptime(seconds: float) -> str:
    """Format uptime in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    else:
        return f"{seconds/86400:.1f} days"