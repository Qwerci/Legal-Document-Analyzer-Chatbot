from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import os
from services.embeddings import index_documents
from services.ocr import extract_text_from_pdf
from database import get_db
from models import Document

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter()

@router.post("/")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = extract_text_from_pdf(filepath)
    
    new_doc = Document(filename=file.filename, filepath=filepath, text_content=extracted_text)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    index_documents(db)

    return {"message": "File uploaded successfully", "document_id": new_doc.id, "extracted_text": extracted_text[:500]}
