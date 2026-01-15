from fastapi import FastAPI
from api.routes import auth, transactions

app = FastAPI(title='Personal Finance Tracker API')

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(transactions.router, prefix='/transactions', tags=['transactions'])
