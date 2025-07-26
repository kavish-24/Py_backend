import fitz  
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile) -> str:
    contents = await file.read()
    with fitz.open(stream=contents, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text.strip()
