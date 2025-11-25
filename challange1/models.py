from pydantic import BaseModel

class BooksCreate(BaseModel):
    title:str
    director:str

class Books(BooksCreate):
    id:int