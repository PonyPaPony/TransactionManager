import pytest
from utils.validators import Validators


def test_check_amount_valid():
    Validators.check_amount(100.0)

def test_check_amount_invalid():
    with pytest.raises(ValueError):
        Validators.check_amount(-100.0)
    with pytest.raises(ValueError):
        Validators.check_amount(0)
    with pytest.raises(ValueError):
        Validators.check_amount("100")

def test_check_date_valid():
    is_valid, msg = Validators.check_date("2021-01-01")
    assert is_valid is True
    assert msg is None

def test_check_date_invalid():
    is_valid, msg = Validators.check_date("3000-01-01")
    assert is_valid is False
    assert "в будущем" in msg

def test_check_date_invalid_format():
    is_valid, msg = Validators.check_date("01-01-2025")
    assert is_valid is False
    assert "формате YYYY-MM-DD" in msg