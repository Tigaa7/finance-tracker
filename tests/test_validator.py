import sys
import os

repository_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(repository_root)
sys.path.append(os.path.join(repository_root, 'src'))

import pytest
from validator import (validate_amount, validate_type,
                       validate_category, validate_date)

def test_valid_amount_returns_float():
    assert validate_amount("50.00") == 50.0

def test_amount_rejects_zero():
    with pytest.raises(ValueError):
        validate_amount("0")

def test_amount_rejects_negative():
    with pytest.raises(ValueError):
        validate_amount("-10")  

def test_amount_rejects_text():
    with pytest.raises(ValueError):
        validate_amount("Hello")

def test_type_accepts_income():
    assert validate_type("income") == "income"

def test_type_accepts_expense():
    assert validate_type("expense") == "expense"

def test_type_is_case_incensitive():
    assert validate_type("income") == "income"
    assert validate_type("Expense") == "expense"

def test_type_rejects_invalid():
    with pytest.raises(ValueError):
        validate_type("profit")

def test_category_accept_valid():
    assert validate_category("Food") == "Food"

def test_category_reject_invalid():
    with pytest.raises(ValueError):
        validate_category("Shopping")


def test_category_rejects_unknown():
    with pytest.raises(ValueError):
        validate_category("Unknown")


def test_date_rejects_plain_text():
    with pytest.raises(ValueError):
        validate_date("today")