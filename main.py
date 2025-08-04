from fastapi import FastAPI, UploadFile, Form, HTTPException,Path
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import extract_text_from_pdf
from scorer import compute_resume_score
from search import search_jobs_by_query
from normalize import normalize_tags, normalize_text
from jd_matcher import router as jd_matcher_router
from pydantic import BaseModel
from typing import List
import uvicorn
import json
from extractor import extract_skills_light






app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store jobs globally to avoid reloading
jobs_data = []


class ApplyRequest(BaseModel):
    job_tags: List[str]

class JobResponse(BaseModel):
    id: str
    title: str
    tags: List[str]


class SearchResponse(BaseModel):
    results: List[JobResponse]

@app.post("/apply")
async def apply_resume(file: UploadFile, job_tags: str = Form(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    resume_text = await extract_text_from_pdf(file)
    normalized_tags = normalize_tags(job_tags.split(","))    
    score = compute_resume_score(resume_text, normalized_tags)
    return {"score": score}


app.include_router(jd_matcher_router, prefix="/match")


@app.post("/live_search")
async def live_search(query: str = Form(...), jobs_json: str = Form(...)):
    try:
        jobs_list = json.loads(jobs_json)
        for job in jobs_list:
            job["tags"] = normalize_tags(job["tags"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid job list JSON: {e}")

    normalized_query = normalize_text(query)
    results = search_jobs_by_query(normalized_query, jobs_list)

    # Return only necessary fields
    final_results = [
        {
            "id": job.get("id", ""),
            "title": job.get("title", ""),
            "tags": job.get("tags", [])
        }
        for job in results
    ]
    return {"results": final_results}


@app.post("/extract")
async def extract_skills_light_route(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF supported.")
    text = await extract_text_from_pdf(file)
    skills = extract_skills_light(text)
    return {"skills": skills}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)