"""FastAPI application for rumor detection."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator

from app.model import predict

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent

app = FastAPI(
    title="Rumor Detection API",
    description="Detect whether a piece of text is a rumor or factual content.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class DetectRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("text must not be empty")
        return v


class DetectResponse(BaseModel):
    label: str
    confidence: float
    rumor_probability: float


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the main web interface."""
    return templates.TemplateResponse(request, "index.html")


@app.post("/api/detect", response_model=DetectResponse)
async def detect(body: DetectRequest) -> DetectResponse:
    """Analyze *text* and return a rumor-detection prediction."""
    result = predict(body.text)
    return DetectResponse(**result)


@app.get("/api/health")
async def health() -> dict:
    """Health-check endpoint."""
    return {"status": "ok"}
