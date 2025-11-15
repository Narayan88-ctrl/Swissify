#!/usr/bin/env bash
cd ~/Swissify
# activate venv
source .venv_swissify/bin/activate
# start engine in background (log to engine.log)
nohup uvicorn swissify_engine.main:app --port 8600 --host 127.0.0.1 > ~/Swissify/engine.log 2>&1 &
# start web
nohup uvicorn swissify_web.main_web:app --port 8601 --host 127.0.0.1 > ~/Swissify/web.log 2>&1 &
# (optional) start school
# nohup uvicorn swissify_school.main_school:app --port 8602 --host 127.0.0.1 > ~/Swissify/school.log 2>&1 &
echo "Services started. Check engine.log and web.log"
