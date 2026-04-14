# 🔍 Rumor Detector

A web-based rumor / fake-news detection application built with **FastAPI** and **scikit-learn**.

## Features

- Paste any text and get an instant prediction: **Likely a Rumor** or **Likely Factual**
- Visual probability meter and model confidence score
- REST API (`POST /api/detect`) for programmatic access
- Lightweight TF-IDF + Logistic Regression model — no external model files needed
- Fully responsive UI built with plain HTML / CSS / JS

## Screenshots

| Empty state | Rumor detected | Factual content |
|---|---|---|
| ![Home](https://github.com/user-attachments/assets/52845611-b11c-4f4a-b5ca-e279fb09369b) | ![Rumor](https://github.com/user-attachments/assets/89767d8b-91fe-4531-a761-88f8df2ec915) | ![Factual](https://github.com/user-attachments/assets/755d191a-4c6c-4776-b5fe-b0c586249cff) |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn app.main:app --reload

# 3. Open http://localhost:8000 in your browser
```

## API

### `POST /api/detect`

**Request**
```json
{ "text": "Your text here" }
```

**Response**
```json
{
  "label": "rumor",           // "rumor" | "not_rumor"
  "confidence": 0.6183,       // model certainty [0, 1]
  "rumor_probability": 0.6183 // probability of being a rumor [0, 1]
}
```

### `GET /api/health`

Returns `{"status": "ok"}` when the service is running.

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI application & routes
│   ├── model.py         # TF-IDF + Logistic Regression pipeline
│   ├── templates/
│   │   └── index.html   # Main web interface
│   └── static/
│       ├── style.css
│       └── script.js
├── tests/
│   └── test_main.py     # pytest test suite
└── requirements.txt
```

## Running Tests

```bash
pytest tests/ -v
```
