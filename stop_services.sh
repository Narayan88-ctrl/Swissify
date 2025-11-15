#!/usr/bin/env bash
# Safely stop all Swissify services (engine, web, school)

kill -9 $(lsof -ti:8601) 2>/dev/null || true
kill -9 $(lsof -ti:8600) 2>/dev/null || true
kill -9 $(lsof -ti:8602) 2>/dev/null || true
pkill -f uvicorn 2>/dev/null || true
echo "✅ All Swissify services stopped."
