from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.embeddings import search_documents
from models import Document

router = APIRouter()

@router.get("/")
def search_legal_documents(query: str, db: Session = Depends(get_db)):
    results = search_documents(query)

    # Fetch document details
    response = []
    for result in results:
        doc = db.query(Document).filter(Document.id == result["document_id"]).first()
        if doc:
            response.append({
                "document_id": doc.id,
                "filename": doc.filename,
                "snippet": doc.text_content[:300],
                "score": result["score"]
            })

    return {"query": query, "results": response}
