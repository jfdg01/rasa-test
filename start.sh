#!/bin/bash

# Startup script for Rasa Wizard Game
echo "🧙 Starting Rasa Wizard Game..."

# Start Rasa Action Server in background
echo "Starting Rasa Action Server on port 5055..."
rasa run actions --port 5055 &
ACTION_PID=$!

# Wait for action server to be ready
echo "Waiting for action server to start..."
sleep 10

# Start Rasa Server in background
echo "Starting Rasa Server on port 5005..."
rasa run --enable-api --cors "*" --port 5005 &
RASA_PID=$!

# Wait for Rasa server to be ready
echo "Waiting for Rasa server to start..."
sleep 10

# Start simple HTTP server for the web UI
echo "Starting Web UI on port 8080..."
python -m http.server 8080 &
WEB_PID=$!

echo ""
echo "✅ All services started!"
echo "   - Web UI: http://localhost:8080/game_ui.html"
echo "   - Rasa API: http://localhost:5005"
echo "   - Actions: http://localhost:5055"
echo ""

# Keep the script running and forward signals
trap "kill $ACTION_PID $RASA_PID $WEB_PID; exit" SIGINT SIGTERM

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?

