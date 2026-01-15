from pydantic import BaseModel
from typing import Optional

class TransactionSchema(BaseModel):
    username: str
    type: str
    category: str
    amount: float
    date: Optional[str] = None
