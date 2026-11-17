# create a virtual environmenent
# activate the environment 

from pathlib import Path
from uuid import uuid4

from fastapi import File, Form, UploadFile

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

app = FastAPI()
from app import repositories
from app.db import get_db


UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"


@app.post("/videos/upload", status_code=201)
async def upload_video(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    suffix = Path(file.filename or "").suffix.lower()
    allowed_suffixes = {".mp4", ".mov", ".mkv"}

    if suffix not in allowed_suffixes:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Try MP4, MOV, or MKV.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    saved_path = UPLOAD_DIR / f"{uuid4()}{suffix}"

    try:
        with saved_path.open("wb") as destination:
            while chunk := await file.read(1024 * 1024):
                destination.write(chunk)

        video = repositories.create_video(
            db,
            title=title,
            source_path=str(saved_path),
            manifest_path=None,
        )
    except Exception:
        saved_path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()

    return {"id": video.id, "title": video.title, "status": video.status}

@app.get("/health")
def get_health():
    return {"status" : "ok"}
@app.post("/videos", status_code=201)
def create_video(title: str, db: Session = Depends(get_db)):
    video = repositories.create_video(db, title=title, manifest_path=None)
    return {"id": video.id, "title": video.title}


@app.get("/videos/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)):
    video = repositories.get_video(db, video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="video not found")
    return {"id": video.id, "title": video.title, "status": video.status}


@app.get("/v1.0/manifest")
def get_manifest(ItemID: int, db: Session = Depends(get_db)):
    video = repositories.get_video(db, ItemID)
    if video is None or video.manifest_path is None:
        raise HTTPException(status_code=404, detail="manifest not found")
    return FileResponse(video.manifest_path, media_type="application/vnd.apple.mpegurl")


@app.get("/v1.0/showfeed")
def show_feed(UserID: int, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    videos = repositories.list_videos(db, limit=limit, offset=offset)
    return {"user_id": UserID, "videos": [{"id": v.id, "title": v.title} for v in videos]}