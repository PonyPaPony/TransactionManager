import pytest
from models.transaction import Transaction

def test_transaction_creation():
    """Проверяем успешное создание транзакции"""
    tx = Transaction("income", 100.0, "salary", "2025-01-01", "bonus")
    assert tx.type == "income"
    assert tx.amount == 100.0
    assert tx.category == "salary"
    assert tx.date == "2025-01-01"
    assert tx.comment == "bonus"

def test_transaction_invalid_amount():
    with pytest.raises(ValueError):
        Transaction("expense", -100, "food", "2021-01-01")

def test_transaction_to_dict():
    tx = Transaction("expense", 50.0, "food", "2025-01-01")
    data = tx.to_dict()
    assert data == {
        "type": "expense",
        "amount": 50.0,
        "category": "food",
        "date": "2025-01-01",
        "comment": None  # Этого не хватало
    }
