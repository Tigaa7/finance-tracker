import re
from datetime import datetime
from models import CATEGORIES

def validate_amount(value):
    """"Check amount is a positive number."""
    try:
        amount = float(value)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        return amount
    except ValueError:
        raise ValueError("Amount must be a positive number e.g. 50.00")

def validate_type(value):
    """Check type is either 'income' or 'expense'."""
    if value.lower() not in ("income", "expense"):
        raise ValueError("Type must be 'income' or 'expense'.")
    return value.lower()

def validate_category(value):
    """Check category is valid."""
    if value not in CATEGORIES:
        raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")
    return value

def validate_date(value):
    """Check date is in correct format."""
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")