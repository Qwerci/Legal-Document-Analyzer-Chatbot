from pydantic import BaseModel
from datetime import datetime

class DocumentSchema(BaseModel):
    filename: str
    text_content: str | None = None
    uploaded_at: datetime

    class Config:
        from_attributes = True
