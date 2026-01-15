from fastapi import APIRouter, HTTPException
from analysis.finance_utils import register_user, login_user

router = APIRouter()

@router.post('/register')
def register(username: str, password: str):
    if not username or not password:
        raise HTTPException(status_code=400, detail='username and password required')
    success = register_user(username, password)
    if success:
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=409, detail='Username already exists')

@router.post('/login')
def login(username: str, password: str):
    if login_user(username, password):
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail='Invalid username or password')
