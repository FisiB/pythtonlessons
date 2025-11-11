from pydantic import BaseModel

class MovieCreate(BaseModel):
    title:str
    writer:str
class Movie(MovieCreate):
    id:int