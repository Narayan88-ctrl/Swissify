#!/bin/bash
cd ~/Swissify/swissify_engine
source ~/Swissify/.venv_swissify/bin/activate
nohup uvicorn main:app --port 8600 > ~/Swissify/engine.log 2>&1 &

cd ~/Swissify/swissify_web
nohup uvicorn main_web:app --port 8601 > ~/Swissify/web.log 2>&1 &
echo "✅ Swissify Engine + Web started successfully!"
