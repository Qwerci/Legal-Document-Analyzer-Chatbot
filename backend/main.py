from fastapi import FastAPI
from database import Base, engine
from routes import upload, search, chat
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal AI Document Analyzer")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload.router, prefix="/api/upload")
app.include_router(search.router, prefix="/api/search")
app.include_router(chat.router, prefix="/api/chat")

@app.get("/")
def root():
    return {"message": "Legal AI API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)