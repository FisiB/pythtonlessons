from pydantic import BaseModel
from typing import Optional,List

class Developer(BaseModel):
    name:str
    experience:Optional[int]=None

class Project(BaseModel):
    title:str
    descritpion:Optional[str]=None
    languages:Optional[List[str]]=[]
    lead_developer:Developer
