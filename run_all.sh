#!/usr/bin/env bash
set -e

source ~/Swissify/.venv_swissify/bin/activate 2>/dev/null || true

# Kill old servers
kill -9 $(lsof -ti:8600) 2>/dev/null || true
kill -9 $(lsof -ti:8601) 2>/dev/null || true
kill -9 $(lsof -ti:8602) 2>/dev/null || true

# Install deps (idempotent)
pip install -r ~/Swissify/swissify_engine/requirements.txt
pip install -r ~/Swissify/swissify_web/requirements.txt
pip install -r ~/Swissify/swissify_school/requirements.txt

# Start three apps
(cd ~/Swissify/swissify_engine && uvicorn main:app --port 8600 --reload) & echo "Engine 8600 started"
sleep 1
(cd ~/Swissify/swissify_web && uvicorn main_web:app --port 8601 --reload) & echo "Web 8601 started"
sleep 1
(cd ~/Swissify/swissify_school && uvicorn main_school:app --port 8602 --reload) & echo "School 8602 started"

echo "All up:
  Engine: http://127.0.0.1:8600/health
  Web UI: http://127.0.0.1:8601/?lang=en
  School: http://127.0.0.1:8602/"
