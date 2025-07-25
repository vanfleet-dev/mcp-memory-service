"""
FastAPI dependencies for the HTTP interface.
"""

from typing import Optional
from fastapi import HTTPException

from ..storage.sqlite_vec import SqliteVecMemoryStorage

# Global storage instance
_storage: Optional[SqliteVecMemoryStorage] = None


def set_storage(storage: SqliteVecMemoryStorage) -> None:
    """Set the global storage instance."""
    global _storage
    _storage = storage


def get_storage() -> SqliteVecMemoryStorage:
    """Get the global storage instance."""
    if _storage is None:
        raise HTTPException(status_code=503, detail="Storage not initialized")
    return _storage