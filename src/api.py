import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import (init_db, add_transaction, get_all_transactions, 
                      get_by_category, monthly_report, update_transaction, delete_transaction as db_delete_transaction)
from models import Transaction as DBTransaction

app = FastAPI(title="Finance Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

# Pydantic model for API requests
class TransactionRequest(BaseModel):
    amount: float
    type: str  # "income" or "expense"
    category: str
    description: Optional[str] = None
    date: Optional[str] = None

@app.post("/transactions")
def create_transaction(tx: TransactionRequest):
    try:
        # Convert Pydantic model to database Transaction model
        db_tx = DBTransaction(
            amount=tx.amount,
            type=tx.type,
            category=tx.category,
            description=tx.description or "",
            date=tx.date or str(date.today())
        )
        add_transaction(db_tx)
        return {"message": "Transaction saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions")
def get_transactions():
    try:
        rows = get_all_transactions()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.put("/transactions/{tx_id}")
def edit_transaction(tx_id: int, body: TransactionRequest):
    try:
        update_transaction(tx_id, body.amount, body.type, body.category, 
                           body.description or "", body.date or str(date.today()))
        return {"message": f"Transaction {tx_id} updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/transactions/{tx_id}")
def remove_transaction(tx_id: int):
    try:
        db_delete_transaction(tx_id)
        return {"message": f"Transaction {tx_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions/category/{category}")
def by_category(category: str):
    try:
        rows = get_by_category(category)
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/report/{year}/{month}")
def report(year: int, month: int):
    try:
        income, expenses, breakdown = monthly_report(year, month)
        return {
            "year": year,
            "month": month,
            "income": income,
            "expenses": expenses,
            "balance": income - expenses,
            "breakdown": [dict(r) for r in breakdown]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
