import re
from typing import List

def normalize_text(text: str) -> str:
    """
    Lowercase, remove punctuation and extra spaces.
    """
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def compute_resume_score(resume_text: str, job_tags: List[str]) -> float:
    """
    Compute match score between a resume and job skills based on skill coverage.
    
    Args:
        resume_text (str): Full resume text.
        job_tags (List[str]): List of job-related tags/keywords.
    
    Returns:
        float: match score (0-100 based on how many skills were found).
    """
    if not resume_text or not job_tags:
        return 0.0

    try:
        resume_text_norm = normalize_text(resume_text)
        job_tags_norm = [normalize_text(tag) for tag in job_tags]

        # Count how many tags are found in the resume
        matched = [tag for tag in job_tags_norm if tag in resume_text_norm]
        score = round(len(matched) / len(job_tags_norm) * 100, 2) if job_tags_norm else 0.0

        return score

    except Exception as e:
        print(f"Error computing score: {e}")
        return 0.0
