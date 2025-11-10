# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Train the Rasa model (optional - comment out if model is pre-trained)
# RUN rasa train --fixed-model-name game_model

# Expose ports
# 5005 for Rasa server
# 5055 for Rasa actions server
# 8080 for web UI
EXPOSE 5005 5055 8080

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Starting Rasa Action Server..."\n\
rasa run actions --port 5055 &\n\
\n\
echo "Waiting for action server to start..."\n\
sleep 5\n\
\n\
echo "Starting Rasa Server..."\n\
rasa run --enable-api --cors "*" --port 5005 &\n\
\n\
echo "Starting Web Server..."\n\
python -m http.server 8080\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start all services
CMD ["/app/start.sh"]

