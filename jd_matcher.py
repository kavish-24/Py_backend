# routes/jd_matcher.py (or just jd_matcher.py if you prefer flat structure)
from fastapi import APIRouter, UploadFile, File, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt
from pdfminer.high_level import extract_text
import nltk
import re

nltk.download('stopwords')
from nltk.corpus import stopwords

router = APIRouter()

def extract_text_file(file: UploadFile):
    try:
        if file.filename.endswith('.pdf'):
            content = extract_text(file.file)
        elif file.filename.endswith('.docx'):
            content = docx2txt.process(file.file)
        else:
            raise ValueError("Unsupported file format.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return content

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    stops = set(stopwords.words('english'))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stops]
    return ' '.join(tokens)

def get_match_score(jd, resume):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([jd, resume])
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return float(score[0][0]) * 100

@router.post("/score")
async def score_resumes(
    ideal: UploadFile = File(...),
    candidate: UploadFile = File(...)
):
    ideal_text = clean_text(extract_text_file(ideal))
    candidate_text = clean_text(extract_text_file(candidate))
    score = get_match_score(ideal_text, candidate_text)
    return {"similarity_score_percent": round(score, 2)}
