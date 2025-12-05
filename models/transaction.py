from datetime import datetime
from utils.validators import Validators


class Transaction:
    def __init__(self, t_type: str, amount: float, category: str, date: str, comment: str = None):
        """
        Инициализация транзакции.
        :param t_type: Тип транзакции ('income' или 'expense')
        :param amount: Сумма
        :param category: Категория
        :param date: Дата в формате 'YYYY-MM-DD'
        :param comment: Комментарий (может быть None)
        """
        Validators.check_amount(amount)

        is_valid_date, date_error = Validators.check_date(date)
        if not is_valid_date:
            raise ValueError(f"Некорректная дата: {date_error}")

        if t_type not in ['income', 'expense']:
            raise ValueError("Тип должен быть 'income' или 'expense'")

        self.type = t_type
        self.amount = amount
        self.category = category
        self.date = date
        self.comment = comment

    def to_dict(self):
        """
        Превращает объект класса в словарь (для записи в JSON).
        """
        return {
            'type': self.type,
            'amount': self.amount,
            'category': self.category,
            "date": self.date,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Создает объект класса из словаря (при чтении из JSON).
        """
        return cls(
            t_type=data['type'],
            amount=data['amount'],
            category=data['category'],
            date=data['date'],
            comment=data.get('comment')
        )

    def __str__(self):
        """
        Красивый вывод для пользователя.
        Пример: [12-05] 💰 Доход +12 500₽ | Категория: Зарплата
        """
        try:
            dt_obj = datetime.strptime(self.date, "%Y-%m-%d")
            date_str = dt_obj.strftime("%d-%m")
        except ValueError:
            date_str = self.date

        if self.type == 'income':
            icon = "💰"
            type_name = "Доход"
            sign = "+"
        else:
            icon = "💸"
            type_name = "Расход"
            sign = "-"

        amount_str = f"{self.amount:,.2f}".replace(",", " ").replace(".", ",")
        result = f"[{date_str}] {icon} {type_name} {sign}{amount_str}$ | Категория: {self.category}"

        if self.comment:
            result += f" | Коммент: {self.comment}"

        return result

    def __lt__(self, other):
        return self.date < other.date
