from fastapi import APIRouter, HTTPException
from api.schemas.transaction import TransactionSchema
from analysis.finance_utils import add_transaction, get_transactions

router = APIRouter()

@router.post('/')
def create_transaction(transaction: TransactionSchema):
    if not transaction.username:
        raise HTTPException(status_code=400, detail='username required')
    add_transaction(transaction.username, transaction.type, transaction.category, transaction.amount, transaction.date)
    return {"message": "Transaction added successfully"}

@router.get('/{username}')
def list_transactions(username: str):
    df = get_transactions(username)
    return df.to_dict(orient='records')
