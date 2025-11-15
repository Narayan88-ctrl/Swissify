#!/usr/bin/env bash
kill -9 $(lsof -ti:8600) 2>/dev/null || true
kill -9 $(lsof -ti:8601) 2>/dev/null || true
kill -9 $(lsof -ti:8602) 2>/dev/null || true
echo "🛑 Stopped 8600/8601/8602."
