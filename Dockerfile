# ==============================================================================
# DOCKERFILE - Celebrity Face Detect AI Agent
# ==============================================================================
#
# BUILD COMMAND:
#   docker build -t face-detect-ai-agent .
#
# RUN COMMAND:
#   docker run -p 5000:5000 --env-file .env face-detect-ai-agent
#
# FOR KUBERNETES (GCP):
#   docker build -t your-dockerhub-username/face-detect-ai-agent:latest .
#   docker push your-dockerhub-username/face-detect-ai-agent:latest
# ==============================================================================

# Use Python 3.12 slim image (matches pyproject.toml requires-python >= 3.12)
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# - Prevents Python from writing .pyc bytecode files to disk
# - Ensures stdout/stderr logs appear immediately (no buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# - build-essential : compiling Python packages that need C extensions
# - curl            : used for health checks
# - libgl1          : required by OpenCV (cv2) for GUI/rendering functions
# - libglib2.0-0    : required by OpenCV for GLib support
# - libsm6          : required by OpenCV (X11 session management)
# - libxext6        : required by OpenCV (X11 extensions)
# - libxrender-dev  : required by OpenCV (X11 rendering)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager, replaces pip)
RUN pip install --no-cache-dir uv

# Copy dependency files FIRST (Docker layer caching optimization)
# - If only source code changes, Docker reuses the cached dependency layer
# - Dependencies are only re-installed when pyproject.toml or uv.lock changes
COPY pyproject.toml .
COPY uv.lock* ./

# Install Python dependencies using uv (fast & reproducible)
RUN uv sync --no-dev --frozen

# Copy the rest of the application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Health check - Docker/Kubernetes uses this to verify the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the Flask application using uv
CMD ["uv", "run", "app.py"]