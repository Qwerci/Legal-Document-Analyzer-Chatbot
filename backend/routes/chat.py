from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.chatbot import legal_chatbot

router = APIRouter()

@router.get("/")
def chat_with_legal_ai(question: str, db: Session = Depends(get_db)):
    response = legal_chatbot(question, db)
    return response
