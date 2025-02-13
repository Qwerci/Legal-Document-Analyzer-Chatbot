import faiss
import numpy as np
from requests import Session
from sentence_transformers import SentenceTransformer
from models import Document


embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# FAISS index will store vectors for fast similarity search
dimension = 384
faiss_index = faiss.IndexFlatL2(dimension)

# Store documents ID mappings
document_ids = []

def generate_embedding(text: str) -> np.ndarray:
    """Convert text into a vector embedding."""
    return embedding_model.encode(text, convert_to_numpy=True)

def index_documents(db: Session):
    """Index all legal documents into FAISS."""
    global document_ids
    documents = db.query(Document).all()

    # Extract text and IDs
    texts = [doc.text_content for doc in documents if doc.text_content]
    document_ids = [doc.id for doc in documents if doc.text_content]

    # Compute embeddings
    if texts:
        embeddings = np.array([generate_embedding(text) for text in texts])
        faiss_index.add(embeddings)


def search_documents(query: str, top_k=5):
    """Find the most relevant legal documents using FAISS similarity search."""
    query_vector = generate_embedding(query).reshape(1, -1)
    distance, indices = faiss_index.search(query_vector, top_k)

    results = []
    for i, index in enumerate(indices[0]):
        if index < len(document_ids):
            results.append({"document_id": document_ids[index], "score": distance[0][i]})
    
    return results
