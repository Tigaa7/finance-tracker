from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    amount: float
    type: str  # "income" or "expenses"
    category: str
    description: str
    date: str   # format: "DD-MM-YY"
    id: int = None # set by database automatically
    created_at: str = None # set by database automatically

CATEGORIES = [
    "Salary", "Food", "Transport",
    "Airtime", "Rent", "Entertainment", "Other"
]