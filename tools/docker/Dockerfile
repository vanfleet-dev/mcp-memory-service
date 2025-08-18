# Platform-agnostic Docker support with UV integration
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    MCP_MEMORY_STORAGE_BACKEND=sqlite_vec \
    MCP_MEMORY_SQLITE_PATH=/app/sqlite_db \
    MCP_MEMORY_BACKUPS_PATH=/app/backups \
    PYTHONPATH=/app/src \
    DOCKER_CONTAINER=1 \
    CHROMA_TELEMETRY_IMPL=none \
    ANONYMIZED_TELEMETRY=false

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy essential files
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY scripts/install_uv.py .

# Install UV
RUN python install_uv.py

# Create directories for data persistence
RUN mkdir -p /app/sqlite_db /app/backups

# Copy source code
COPY src/ /app/src/
COPY scripts/utils/uv_wrapper.py scripts/utils/memory_wrapper_uv.py ./
COPY run_server.py ./
COPY tools/docker/docker-entrypoint.sh /usr/local/bin/
COPY tools/docker/docker-entrypoint-persistent.sh /usr/local/bin/
COPY tools/docker/docker-entrypoint-unified.sh /usr/local/bin/

# Install the package with UV
RUN python -m uv pip install -e .

# Pre-download embedding models to prevent runtime download issues
RUN python -c "from sentence_transformers import SentenceTransformer; \
    print('Pre-downloading embedding models...'); \
    SentenceTransformer('all-MiniLM-L6-v2'); \
    print('Embedding models cached successfully')"

# Configure stdio for MCP communication and make entrypoints executable
RUN chmod a+rw /dev/stdin /dev/stdout /dev/stderr && \
    chmod +x /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint-persistent.sh && \
    chmod +x /usr/local/bin/docker-entrypoint-unified.sh

# Add volume mount points for data persistence
VOLUME ["/app/sqlite_db", "/app/backups"]

# Expose the port (if needed)
EXPOSE 8000

# Use the unified entrypoint script by default
# Can be overridden with docker-entrypoint.sh for backward compatibility
ENTRYPOINT ["/usr/local/bin/docker-entrypoint-unified.sh"]
