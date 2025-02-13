from fastapi import FastAPI
from database import Base, engine
from routes import upload, search

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal AI Document Analyzer")

app.include_router(upload.router, prefix="/api/upload")
# app.include_router(search.router, prefix="/api/search")

@app.get("/")
def root():
    return {"message": "Legal AI API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)