from datetime import datetime


class Validators:
    @staticmethod
    def check_amount(amount: float):
        if amount <= 0:
            print("Сумма должна быть больше 0")
            raise ValueError

    @staticmethod
    def check_date(date: str):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
