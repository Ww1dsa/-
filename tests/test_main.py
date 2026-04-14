"""Tests for the FastAPI rumor-detection application."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

def test_health_ok():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

def test_index_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Rumor Detector" in response.text


# ---------------------------------------------------------------------------
# Detect endpoint – valid inputs
# ---------------------------------------------------------------------------

def test_detect_rumor_text():
    """Highly sensational, forwarded-message style text should be classified as a rumor."""
    rumor_text = (
        "BREAKING: Scientists discover that drinking coffee causes instant blindness, "
        "share before deleted!"
    )
    response = client.post("/api/detect", json={"text": rumor_text})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "rumor"
    assert 0.0 <= data["rumor_probability"] <= 1.0
    assert 0.0 <= data["confidence"] <= 1.0


def test_detect_factual_text():
    """Source-attributed, measured scientific language should be classified as not a rumor."""
    factual_text = (
        "According to a peer-reviewed study published in Nature, regular exercise "
        "reduces heart disease risk by 30%."
    )
    response = client.post("/api/detect", json={"text": factual_text})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "not_rumor"
    assert 0.0 <= data["rumor_probability"] <= 1.0
    assert 0.0 <= data["confidence"] <= 1.0


def test_detect_response_schema():
    """Response must contain the three expected fields with correct types."""
    response = client.post("/api/detect", json={"text": "Some test text."})
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"label", "confidence", "rumor_probability"}
    assert data["label"] in ("rumor", "not_rumor")
    assert isinstance(data["confidence"], float)
    assert isinstance(data["rumor_probability"], float)


# ---------------------------------------------------------------------------
# Detect endpoint – invalid inputs
# ---------------------------------------------------------------------------

def test_detect_missing_text_field():
    """Request body without 'text' field should return 422 Unprocessable Entity."""
    response = client.post("/api/detect", json={})
    assert response.status_code == 422


def test_detect_empty_string():
    """Empty string should return a validation error."""
    response = client.post("/api/detect", json={"text": ""})
    assert response.status_code == 422


def test_detect_whitespace_only():
    """Whitespace-only string should return a validation error."""
    response = client.post("/api/detect", json={"text": "   "})
    assert response.status_code == 422


def test_detect_non_string_text():
    """Non-string 'text' value should return 422 (Pydantic v2 does not coerce integers to str)."""
    response = client.post("/api/detect", json={"text": 12345})
    assert response.status_code == 422
