# Dockerfile for Cursor Automation System Builder MCP Server
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY mcp_requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r mcp_requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=.
ENV PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start the server
CMD ["python", "-m", "app.mcp.simple_http_server"]
