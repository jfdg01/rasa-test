# Use Python 3.10.11 as base image
FROM python:3.10.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    bash \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# The model is pre-trained and located in models/ directory
# Rasa will automatically use the latest model from models/ when starting

# Ensure startup script is executable
RUN chmod +x /app/start.sh

# Expose ports
# 5005 for Rasa server
# 5055 for Rasa actions server  
# 8080 for web UI
EXPOSE 5005 5055 8080

# Health check to verify services are running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5005/status || exit 1

# Use exec form for proper signal handling
# This ensures signals are properly forwarded to the script
CMD ["/bin/bash", "/app/start.sh"]

