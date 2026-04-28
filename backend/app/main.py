from fastapi import FastAPI, UploadFile
from app.services.azure_blob import upload_file, download_file
from app.utils.pdf_worker import extract_text_from_pdf
from app.agents.parser import parse_cv
from app.agents.grader import grade_user
from app.agents.roadmap import generate_roadmap
from app.services.vector_db import match_jobs

app = FastAPI()

@app.post("/upload-cv")
async def upload_cv(file: UploadFile):
    blob_url = upload_file(file)
    return {"blob_url": blob_url}


@app.post("/process-cv")
async def process_cv(blob_url: str):
    # (Download & Extract text tetep sync nggak masalah klo cepet)
    file_path = download_file(blob_url)
    raw_text = extract_text_from_pdf(file_path)

    parsed = await parse_cv(raw_text)
    
    # Vector matching jalanin biasa karena model lokal
    matches, gaps = match_jobs(parsed)

    # Await AI Grader & Roadmap
    level = await grade_user(parsed, matches)
    roadmap = await generate_roadmap(parsed, gaps, level)

    return {
        "parsed": parsed,
        "matches": matches,
        "gaps": gaps,
        "level": level,
        "roadmap": roadmap
    }