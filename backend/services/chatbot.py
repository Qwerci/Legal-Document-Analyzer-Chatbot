import os
import openai
from sqlalchemy.orm import Session

from backend.models import Document
from services.embeddings import search_documents

openai.api_key = os.getenv("MISTRAL_API_KEY")

def query(prompt: str) -> str:
    """Send a query to LLM API and return a response"""
    response = openai.chat.completions.create(
        models = "open-mistral-nemo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response["choices"][0]["message"]["content"]


def legal_chatbot(question: str, db:Session):
    """Find relevant legal documents and generate AI-powered answers."""
    search_results = search_documents(question)

    context = ""
    for result in search_results:
        doc = db.query(Document).filter(Document.id == result["document_id"]).first()
        if doc:
            context += f"Document: {doc.filename}\nSnippet: {doc.text_content[:1000]}\n\n"

    # Generate AI response
    prompt = f"""
    You are a legal assistant. Answer the following question based on the provided legal documents:
    
    Context:
    {context}

    Question: {question}

    Answer:
    """
    
    ai_response = query(prompt)
    
    return {"question": question, "answer": ai_response, "sources": search_results}