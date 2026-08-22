from fastapi import FastAPI, UploadFile, File
from faster_whisper import WhisperModel
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = WhisperModel("base")


@app.get("/")
def home():
    return {
        "message": "Welcome to Sinhala Transcriber"
    }


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
        "transcript": transcript
    }
