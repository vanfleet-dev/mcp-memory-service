"""
FastAPI application for MCP Memory Service HTTP/SSE interface.

Provides REST API and Server-Sent Events using SQLite-vec backend.
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from ..config import (
    HTTP_PORT,
    HTTP_HOST,
    CORS_ORIGINS,
    DATABASE_PATH,
    EMBEDDING_MODEL_NAME
)
from ..storage.sqlite_vec import SqliteVecMemoryStorage
from .dependencies import set_storage, get_storage
from .api.health import router as health_router

logger = logging.getLogger(__name__)

# Global storage instance
storage: Optional[SqliteVecMemoryStorage] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global storage
    
    # Startup
    logger.info("Starting MCP Memory Service HTTP interface...")
    try:
        storage = SqliteVecMemoryStorage(
            db_path=DATABASE_PATH,
            embedding_model=EMBEDDING_MODEL_NAME
        )
        await storage.initialize()
        set_storage(storage)  # Set the global storage instance
        logger.info(f"SQLite-vec storage initialized at {DATABASE_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize storage: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down MCP Memory Service HTTP interface...")
    if storage:
        await storage.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="MCP Memory Service",
        description="HTTP REST API and SSE interface for semantic memory storage",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(health_router, prefix="/api", tags=["health"])
    
    # Serve static files (dashboard)
    static_path = os.path.join(os.path.dirname(__file__), "static")
    if os.path.exists(static_path):
        app.mount("/static", StaticFiles(directory=static_path), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        """Serve the dashboard homepage."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MCP Memory Service</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>MCP Memory Service</h1>
            <p>HTTP/SSE interface is running!</p>
            <ul>
                <li><a href="/api/health">Health Check</a></li>
                <li><a href="/api/docs">API Documentation</a></li>
                <li><a href="/events">Server-Sent Events</a> (coming soon)</li>
            </ul>
        </body>
        </html>
        """
    
    return app


# Create the app instance
app = create_app()


# Storage getter is now in dependencies.py