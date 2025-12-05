from datetime import datetime


class Validators:
    @staticmethod
    def check_amount(amount: float):
        if not isinstance(amount, (int, float)):
            raise ValueError("Сумма должна быть числом.")
        if amount <= 0:
            raise ValueError("Сумма должна быть больше 0.")

    @staticmethod
    def check_date(date_text: str):
        try:
            dt = datetime.strptime(date_text, "%Y-%m-%d")
        except ValueError:
            return False, "Дата должна быть в формате YYYY-MM-DD."

        if dt.date() > datetime.now().date():
            return False, "Дата не может быть в будущем."

        return True, None
