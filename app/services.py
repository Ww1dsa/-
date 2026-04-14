from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from uuid import uuid4

from fastapi import UploadFile

RUMOR_KEYWORDS = {
    "必死",
    "马上转发",
    "内部消息",
    "震级",
    "封城",
    "100%",
    "速看",
    "紧急通知",
}

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mov"}


def detect_rumor_text(text: str) -> Dict[str, Any]:
    cleaned = (text or "").strip()
    if not cleaned:
        return {
            "level": "未检测",
            "message": "请输入待检测文本。",
            "score": 0.0,
        }

    matched = [kw for kw in RUMOR_KEYWORDS if kw in cleaned]
    score = min(0.99, len(matched) * 0.18 + (0.2 if len(cleaned) > 80 else 0.05))

    if score >= 0.6:
        level = "高风险"
        message = "该内容疑似谣言，请核验来源后再传播。"
    elif score >= 0.35:
        level = "中风险"
        message = "该内容存在争议信息，建议查证后再判断。"
    else:
        level = "低风险"
        message = "暂未发现明显谣言特征，但仍建议多方核验。"

    return {
        "level": level,
        "message": message,
        "score": round(score, 2),
        "matched": matched,
    }


def save_media_file(file: UploadFile, upload_dir: Path) -> Tuple[bool, str, Optional[Path]]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        return False, "文件类型不支持，请上传图片或视频文件。", None

    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}{suffix}"
    file_path = upload_dir / filename

    data = file.file.read()
    if len(data) == 0:
        return False, "文件为空，请重新上传。", None
    if len(data) > 100 * 1024 * 1024:
        return False, "文件超过100MB限制。", None

    file_path.write_bytes(data)

    fake_score = min(0.95, 0.45 + len(data) / (120 * 1024 * 1024))
    verdict = (
        f"鉴别完成：疑似伪造概率 {fake_score * 100:.1f}%（演示版规则结果）。"
    )
    return True, verdict, file_path
