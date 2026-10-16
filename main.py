import os
import uuid
from datetime import datetime

import cv2
from deepface import DeepFace
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./sentinal.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String, unique=True, index=True)
    timestamp = Column(String)
    date = Column(String)
    location = Column(String)
    risk_score = Column(Integer)
    status = Column(String, default="NEW")
    image_path = Column(String)
    gender = Column(String)
    emotion = Column(String)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SENTINAL - Workplace Safety Monitoring Prototype")
os.makedirs("static/evidence", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

current_detection = {
    "human": "WAITING",
    "gender": "---",
    "emotion": "---",
    "risk": 0,
}
_camera = None
_last_saved_alert = None


def analyze_frame(frame):
    """Analyze one frame and store a prototype alert for selected emotions."""
    global current_detection, _last_saved_alert

    try:
        results = DeepFace.analyze(
            frame,
            actions=["gender", "emotion"],
            enforce_detection=False,
        )
        result = results[0] if isinstance(results, list) else results
        emotion = result.get("dominant_emotion", "unknown")
        gender = result.get("dominant_gender", "unknown")

        # Demonstration rule only: this is not harassment detection.
        risk = 95 if emotion in {"angry", "fear", "sad"} else 10
        current_detection = {
            "human": "DETECTED",
            "gender": gender,
            "emotion": emotion,
            "risk": risk,
        }

        # Avoid writing the same alert on every camera frame.
        alert_key = (emotion, risk)
        if risk > 80 and alert_key != _last_saved_alert:
            evidence_id = str(uuid.uuid4())[:8]
            filename = f"ev_{evidence_id}.jpg"
            image_path = f"static/evidence/{filename}"
            if cv2.imwrite(image_path, frame):
                db = SessionLocal()
                try:
                    now = datetime.now()
                    incident = Incident(
                        evidence_id=f"#{evidence_id}",
                        timestamp=now.strftime("%I:%M %p"),
                        date=now.strftime("%b %d, %Y"),
                        location="Demo Camera - Zone 1",
                        risk_score=risk,
                        status="NEW",
                        image_path=f"/static/evidence/{filename}",
                        gender=gender,
                        emotion=emotion,
                    )
                    db.add(incident)
                    db.commit()
                    _last_saved_alert = alert_key
                    print(f"Prototype alert recorded: {incident.evidence_id}")
                finally:
                    db.close()
        elif risk <= 80:
            _last_saved_alert = None

    except Exception as exc:
        # DeepFace may fail when no face is visible or a frame cannot be analyzed.
        current_detection = {
            "human": "SCANNING",
            "gender": "---",
            "emotion": "---",
            "risk": 0,
        }
        print(f"Frame analysis skipped: {exc}")


def get_camera():
    global _camera
    if _camera is None or not _camera.isOpened():
        _camera = cv2.VideoCapture(0)
    return _camera


def gen_frames():
    camera = get_camera()
    while True:
        success, frame = camera.read()
        if not success:
            current_detection.update(
                {"human": "CAMERA UNAVAILABLE", "gender": "---", "emotion": "---", "risk": 0}
            )
            break

        analyze_frame(frame)
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )


@app.get("/", response_class=HTMLResponse)
async def live_detection(request: Request):
    return templates.TemplateResponse("live.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    db = SessionLocal()
    try:
        incidents = db.query(Incident).order_by(Incident.id.desc()).all()
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request, "incidents": incidents},
        )
    finally:
        db.close()


@app.get("/video_feed")
def video_feed():
    return StreamingResponse(
        gen_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@app.get("/api/stats")
def get_stats():
    return current_detection


@app.on_event("shutdown")
def release_camera():
    if _camera is not None and _camera.isOpened():
        _camera.release()
