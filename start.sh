#!/bin/bash
set -euo pipefail

# Startup script for Rasa Wizard Game
echo "🧙 Starting Rasa Wizard Game..."

# Function to handle shutdown gracefully
cleanup() {
    echo ""
    echo "Shutting down services..."
    # Kill all background jobs (more reliable than storing individual PIDs)
    # Use jobs -p to get all background job PIDs
    if [ -n "${ACTION_PID:-}" ] && kill -0 "$ACTION_PID" 2>/dev/null; then
        kill "$ACTION_PID" 2>/dev/null || true
    fi
    if [ -n "${RASA_PID:-}" ] && kill -0 "$RASA_PID" 2>/dev/null; then
        kill "$RASA_PID" 2>/dev/null || true
    fi
    if [ -n "${WEB_PID:-}" ] && kill -0 "$WEB_PID" 2>/dev/null; then
        kill "$WEB_PID" 2>/dev/null || true
    fi
    # Also kill any remaining background jobs
    jobs -p | while read -r pid; do
        kill "$pid" 2>/dev/null || true
    done
    # Wait for processes to terminate
    wait 2>/dev/null || true
    exit 0
}

# Set up signal handlers for graceful shutdown (must be before starting services)
trap cleanup SIGINT SIGTERM EXIT

# Start Rasa Action Server in background
echo "Starting Rasa Action Server on port 5055..."
rasa run actions --port 5055 &
ACTION_PID=$!

# Wait for action server to be ready and verify it's running
echo "Waiting for action server to start..."
sleep 5

# Check if action server process is still running
if ! kill -0 "$ACTION_PID" 2>/dev/null; then
    echo "❌ Error: Action server failed to start"
    exit 1
fi

# Start Rasa Server in background with model from models/ directory
echo "Starting Rasa Server on port 5005 with model from models/ directory..."
rasa run --enable-api --cors "*" --port 5005 --model models/ &
RASA_PID=$!

# Wait for Rasa server to be ready and verify it's running
echo "Waiting for Rasa server to start..."
sleep 5

# Check if Rasa server process is still running
if ! kill -0 "$RASA_PID" 2>/dev/null; then
    echo "❌ Error: Rasa server failed to start"
    exit 1
fi

# Start proxy server for the web UI (also proxies to Rasa API)
# Use Railway's PORT environment variable if available, otherwise default to 8080
WEB_PORT=${PORT:-8080}
echo "Starting Proxy/Web Server on port $WEB_PORT..."
python proxy_server.py $WEB_PORT &
WEB_PID=$!

# Verify web server started
sleep 2
if ! kill -0 "$WEB_PID" 2>/dev/null; then
    echo "❌ Error: Web server failed to start"
    exit 1
fi

echo ""
echo "✅ All services started successfully!"
echo "   - Web UI: http://localhost:$WEB_PORT/game_ui.html"
echo "   - Rasa API: http://localhost:5005"
echo "   - Actions: http://localhost:5055"
echo ""

# Wait for all background processes
# This keeps the container running and forwards signals properly
wait

