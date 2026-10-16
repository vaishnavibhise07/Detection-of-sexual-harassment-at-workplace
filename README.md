# SENTINAL — Workplace Safety Monitoring Prototype

SENTINAL is a **college-project prototype** that demonstrates a webcam-based computer-vision pipeline, a simple emotion-based demo score, local evidence storage, and a browser dashboard.

> **Important limitation:** This project does not detect or verify workplace harassment. It uses DeepFace's predicted facial emotion and a hand-written rule to assign a demonstration score. Facial-expression predictions are uncertain and must not be used as proof of distress, misconduct, or danger.

## Features

- Webcam video stream served by FastAPI
- Facial attribute analysis through DeepFace (emotion and gender prediction)
- Illustrative risk score: `95` for `angry`, `fear`, or `sad`; otherwise `10`
- SQLite storage for locally recorded high-score frames
- Live status panel and evidence dashboard rendered with Jinja2 templates

## Technology stack

- Python
- FastAPI and Uvicorn
- OpenCV
- DeepFace
- SQLAlchemy and SQLite
- HTML, JavaScript, Tailwind CSS CDN
- Jinja2

## Project structure

```text
SENTINAL/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   ├── live.html
│   └── dashboard.html
└── static/
    └── evidence/        # Runtime images are saved here; not committed
```

## Run locally

### 1. Requirements

Use Python 3.10 or 3.11 for the best chance of compatibility with the machine-learning dependencies. A webcam is needed for live camera testing.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Start the app

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000` for the live monitor and `http://127.0.0.1:8000/dashboard` for recorded demo events.

The first DeepFace run may download model weights and can take time. If the webcam cannot be opened, check operating-system camera permissions and ensure another application is not using it.

## How it works

1. The browser requests `/video_feed`.
2. OpenCV reads frames from the local webcam.
3. DeepFace estimates facial attributes for a frame.
4. A simple rule assigns a demonstration score based on the predicted emotion.
5. When the score is high, the frame and event metadata are stored locally.
6. `/api/stats` supplies the latest values to the live page; `/dashboard` displays stored events.

## Known limitations

- This is a prototype, not a validated safety or harassment-detection system.
- Emotion-based scoring can produce false positives and false negatives.
- The code does not identify people, compare identities, or explicitly count all people in a frame.
- The location is a placeholder (`Demo Camera - Zone 1`), not GPS or camera-location detection.
- Alerts are logged to the terminal and saved to a local database; there is no email, SMS, or external notification integration.
- SQLite data and evidence images are local to the machine running the app.
- The app has not been hardened for production, authentication, privacy compliance, or deployment.
- DeepFace's gender and emotion outputs are model predictions and may be inaccurate or biased.
- The alert de-duplication is intentionally simple and is not a production alert-management strategy.

## Privacy and responsible use

Only test with people who have given informed consent. Avoid committing real faces, captured evidence, database files, or other personal data to a public repository. This project should not be used to make employment, disciplinary, or safety decisions.

## For recruiters

This repository demonstrates a learning prototype involving a Python API, webcam frame processing, model inference, a relational database, and a small web interface. The implementation and limitations are documented transparently; it should not be interpreted as a production-ready AI system.

## License

This project is shared for educational and portfolio review. Add a formal license if you want to permit reuse under specific terms.
