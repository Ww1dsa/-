from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .knowledge import AUTHORITY_CHANNELS, LAW_ITEMS, METHOD_ITEMS, RUMOR_PATTERNS
from .models import ForumPost, Report
from .services import detect_rumor_text, save_media_file

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"

app = FastAPI(title="暗流哨卫 - Python版")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "text_result": None,
            "media_result": None,
        },
    )


@app.post("/detect/text", response_class=HTMLResponse)
def detect_text(request: Request, rumor_text: str = Form("")):
    result = detect_rumor_text(rumor_text)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "text_result": result,
            "media_result": None,
            "rumor_text": rumor_text,
        },
    )


@app.post("/detect/media", response_class=HTMLResponse)
def detect_media(request: Request, media_file: UploadFile = File(...)):
    ok, message, saved_path = save_media_file(media_file, UPLOAD_DIR)
    media_result = {
        "ok": ok,
        "message": message,
        "saved_path": str(saved_path.name) if saved_path else None,
    }
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "text_result": None,
            "media_result": media_result,
        },
    )


@app.get("/report", response_class=HTMLResponse)
def report_page(request: Request):
    return templates.TemplateResponse(request, "report.html", {"success": False})


@app.post("/report", response_class=HTMLResponse)
def create_report(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    contact: str = Form(""),
    db: Session = Depends(get_db),
):
    report = Report(title=title.strip(), content=content.strip(), contact=contact.strip())
    db.add(report)
    db.commit()
    return templates.TemplateResponse(request, "report.html", {"success": True})


@app.get("/forum", response_class=HTMLResponse)
def forum_page(request: Request, db: Session = Depends(get_db)):
    posts = db.query(ForumPost).order_by(ForumPost.id.desc()).all()
    return templates.TemplateResponse(request, "forum.html", {"posts": posts})


@app.post("/forum")
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form("匿名用户"),
    db: Session = Depends(get_db),
):
    post = ForumPost(
        title=title.strip(),
        content=content.strip(),
        author=(author or "匿名用户").strip(),
    )
    db.add(post)
    db.commit()
    return RedirectResponse(url="/forum", status_code=303)


@app.get("/knowledge", response_class=HTMLResponse)
def knowledge_page(request: Request):
    return templates.TemplateResponse(
        request,
        "knowledge.html",
        {
            "patterns": RUMOR_PATTERNS,
            "channels": AUTHORITY_CHANNELS,
            "laws": LAW_ITEMS,
            "methods": METHOD_ITEMS,
        },
    )
