import pytest
from unittest.mock import patch
from main import ConsoleApp

cancel_msg = "Cancel"
choice_msg = ["q"]

@pytest.fixture
def app():
    return ConsoleApp()

def test_amount_menu_valid(app):
    with patch("builtins.input", return_value="100"):
        result = app.amount_menu(cancel_msg, choice_msg)
        assert result == pytest.approx(100.0)

def test_amount_menu_cancel(app):
    with patch("builtins.input", return_value="q"):
        result = app.amount_menu(cancel_msg, choice_msg)
        assert result is None

def test_amount_menu_invalid_then_cancel(app):
    # Сценарий: ввели буквы -> ошибка -> цикл -> ввели 'q' -> выход
    with patch("builtins.input", side_effect=["invalid", "q"]):
        result = app.amount_menu(cancel_msg, choice_msg)
        assert result is None

def test_amount_menu_empty_then_valid(app):
    # Сценарий: ничего не ввели -> ошибка -> цикл -> ввели 100 -> успех
    with patch("builtins.input", side_effect=["", "100"]):
        result = app.amount_menu(cancel_msg, choice_msg)
        assert result == pytest.approx(100.0)

def test_category_menu_valid(app):
    with patch("builtins.input", return_value="food"):
        result = app.category_menu(cancel_msg, choice_msg)
        assert result == "food"

def test_category_menu_cancel(app):
    with patch("builtins.input", return_value="q"):
        result = app.category_menu(cancel_msg, choice_msg)
        assert result is None

def test_category_menu_empty_then_valid(app):
    # Пустой ввод -> цикл -> нормальная категория
    with patch("builtins.input", side_effect=["", "food"]):
        result = app.category_menu(cancel_msg, choice_msg)
        assert result == "food"

def test_date_menu_valid(app):
    with patch("builtins.input", return_value="2021-01-01"):
        result = app.date_menu(cancel_msg, choice_msg)
        assert result == "2021-01-01"

def test_date_menu_cancel(app):
    with patch("builtins.input", return_value="q"):
        result = app.date_menu(cancel_msg, choice_msg)
        assert result is None

def test_date_menu_invalid_then_valid(app):
    # Неверный формат даты -> цикл -> верная дата
    with patch("builtins.input", side_effect=["3030-09-08", "2021-01-01"]):
        result = app.date_menu(cancel_msg, choice_msg)
        assert result == "2021-01-01"

def test_date_menu_today(app):
    from datetime import datetime
    today_str = datetime.now().strftime("%Y-%m-%d")
    with patch("builtins.input", return_value="0"):
        result = app.date_menu(cancel_msg, choice_msg)
        assert result == today_str

def test_date_future_then_cancel(app):
    # Дата из будущего -> цикл -> отмена
    with patch("builtins.input", side_effect=["3030-09-08", "q"]):
        result = app.date_menu(cancel_msg, choice_msg)
        assert result is None

def test_comment_menu_valid(app):
    with patch("builtins.input", return_value="bonus"):
        result = app.comment_menu(cancel_msg, choice_msg)
        assert result == "bonus"

def test_comment_menu_cancel(app):
    with patch("builtins.input", return_value="q"):
        result = app.comment_menu(cancel_msg, choice_msg)
        # В main.py при отмене в комменте возвращается спец. Флаг
        assert result == 'CANCEL_ACTION'

def test_comment_menu_empty(app):
    with patch("builtins.input", return_value=""):
        result = app.comment_menu(cancel_msg, choice_msg)
        assert result is None