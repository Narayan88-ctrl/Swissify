# -*- coding: utf-8 -*-
from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pathlib import Path

HERE = Path(__file__).parent

app = FastAPI(title="Swissify School Portal", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(HERE / "static")), name="static")
templates = Jinja2Templates(directory=str(HERE / "templates"))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
