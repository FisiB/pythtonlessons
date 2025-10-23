from pydantic import BaseModel
from typing import List,Optional

class Developer(BaseModel):
    emri:str
    eksperienca:Optional[int] = None

class Projekt(BaseModel):
    title:str
    description:Optional[str]=None
    languages:Optional[List[str]]=[]
    lead_developer:Developer