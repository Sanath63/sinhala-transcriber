from fastapi import FastAPI, UploadFile, File, Request
from faster_whisper import WhisperModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = WhisperModel("base")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    segments, info = model.transcribe(file_path)

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return {
        "filename": file.filename,
        "language": info.language,
        "transcript": transcript.strip()
    }
