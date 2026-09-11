from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from faster_whisper import WhisperModel
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    segments, info = model.transcribe(
    file_path,
    beam_size=5,
    vad_filter=True
)

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return {
        "filename": file.filename,
        "language": info.language,
        "transcript": transcript.strip()
    }
