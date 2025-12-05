import pytest
import os
from services.transaction_manager import TransactionManager
from models.transaction import Transaction


@pytest.fixture
def test_manager():
    manager = TransactionManager()

    manager.file_manager.file_path = './test_data.json'
    manager.file_manager._ensure_file_exists()
    manager.file_manager.write_data([])

    yield manager

    if os.path.exists("./test_data.json"):
        os.remove("./test_data.json")
    if os.path.exists("./test_data.json.tmp"): # На случай если tmp остался
        os.remove("./test_data.json.tmp")

def test_add_transaction(test_manager):
    tx = Transaction("expense", 100, "food", "2021-01-01")
    test_manager.add_transaction(tx)

    all_tx = test_manager.get_all_transactions()
    assert len(all_tx) == 1
    assert all_tx[0].amount == 100


def test_calculate_stats(test_manager):
    test_manager.add_transaction(Transaction("expense", 100, "food", "2021-01-01"))
    test_manager.add_transaction(Transaction("income", 100, "salary", "2021-01-01"))

    stats = test_manager.calculate_stats()

    assert stats["total_income"] == 100
    assert stats["total_expense"] == 100
    assert stats['balance'] == 0
    assert stats['income_categories']['salary'] == 100
    assert stats['expense_categories']['food'] == 100