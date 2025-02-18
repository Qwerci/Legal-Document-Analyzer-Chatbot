import os
from urllib import response
from mistralai import Mistral
from sqlalchemy.orm import Session
import redis
from models import Document
from services.embeddings import search_documents

api_key = os.getenv("MISTRAL_API_KEY")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("PORT")

client = Mistral(api_key=api_key)
redis_client = redis.Redis(host= redis_host, port= redis_port, db=0)

def query(prompt: str) -> str:
    """Send a query to LLM API and return a response"""
    response = client.chat.complete(
        model= "open-mistral-nemo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


def get_cached_response(question: str):
    cached_response = redis_client.get(question)
    if cached_response:
        return cached_response.decode("utf-8")
    return None

def cache_response(question: str, response: str):
    redis_client.setex(question, 3600, response)

def legal_chatbot(question: str, db:Session):
    """check cache before querying model"""
    cache_answer = get_cached_response(question)
    if cache_answer:
        return {"question":question, "answer":cache_answer, "source":[]}

    """Find relevant legal documents and generate AI-powered answers."""
    search_results = search_documents(question)

    context = ""
    for result in search_results:
        doc = db.query(Document).filter(Document.id == result["document_id"]).first()
        if doc:
            summarized_content = summarize_text(doc.text_content[:1000])
            context += f"Document: {doc.filename}\nSummary: {summarized_content}\n\n"

    # Generate AI response
    prompt = f"""
    You are a legal assistant. Answer the question using only the provided legal documents. Be precise and formal.

    Context:
    {context}

    Question: {question}

    **Answer (Provide clear and legally accurate information):**
    """
    
    ai_response = query(prompt)

    cache_response(question, ai_response)
    
    return {"question": question, "answer": ai_response, "sources": search_results}

def summarize_text(text: str) -> str:
    """Summarize the given text using Mistral API."""
    prompt = f"Summarize the following legal document content:\n\n{text}\n\nSummary:"

    response = query(prompt)
    return response.strip()

