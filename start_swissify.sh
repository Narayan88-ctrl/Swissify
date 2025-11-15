#!/usr/bin/env bash
# 🌄 Swissify One-Shot Launcher

# Stop any old processes
kill -9 $(lsof -ti:8600) 2>/dev/null || true
kill -9 $(lsof -ti:8601) 2>/dev/null || true
pkill -f uvicorn 2>/dev/null || true

# Activate environment
source ~/Swissify/.venv_swissify/bin/activate

# Start both servers
echo "🚀 Starting Swissify Engine (port 8600)…"
uvicorn swissify_engine.main:app --port 8600 --reload &
sleep 2

echo "🌐 Starting Swissify Web (port 8601)…"
uvicorn swissify_web.main_web:app --port 8601 --reload &

echo "✅ Swissify Engine + Web running!"
echo "Open 👉 http://127.0.0.1:8601 in your browser."
