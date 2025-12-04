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
        Красивый вывод для отладки (не для пользователя).
        """
        return f"{self.date} | {self.type} | {self.amount} | {self.category}"

    def __lt__(self, other):
        return self.date < other.date
