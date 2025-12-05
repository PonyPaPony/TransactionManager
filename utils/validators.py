from datetime import datetime


class Validators:
    @staticmethod
    def check_amount(amount: float):
        if amount <= 0:
            raise ValueError

    @staticmethod
    def check_date(date_text: str):
        try:
            dt = datetime.strptime(date_text, "%Y-%m-%d")

            if dt.date() > datetime.now().date():
                print("Дата в будущем?")
                return False
            return True
        except ValueError:
            return False
