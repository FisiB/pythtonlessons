from pydantic import BaseModel
from typing import Optional, List

class Writer(BaseModel):
    name: str

class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    lead_writer: Writer

class BookList(BaseModel):
    books: List[BookCreate]
