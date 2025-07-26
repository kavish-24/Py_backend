import re
from skills_list import COMMON_SKILLS

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def extract_skills_light(text: str) -> list:
    """
    Extracts skills from resume text by simple keyword matching.
    """
    text = normalize(text)
    skills_found = []
    for skill in COMMON_SKILLS:
        skill_norm = normalize(skill)
        if skill_norm in text:
            skills_found.append(skill)
    return skills_found
