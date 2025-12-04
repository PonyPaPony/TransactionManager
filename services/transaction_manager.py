from services.file_manager import FileManager
from models.transaction import Transaction
from datetime import datetime, timedelta


class TransactionManager:
    def __init__(self):
        self.file_manager = FileManager()
        self.transactions = self._load_transactions()

    def _load_transactions(self):
        """Вспомогательный метод: читает файл и превращает словари в объекты Transaction"""
        raw_data = self.file_manager.read_data()
        return [Transaction.from_dict(item) for item in raw_data]

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        data_to_save = [t.to_dict() for t in self.transactions]

        self.file_manager.write_data(data_to_save)

    def get_all_transactions(self):
        return sorted(self.transactions, reverse=True)

    def get_filtered_transactions(self, period):
        """
        period: 'today', 'week', 'month' или кортеж (start_date, end_date)
        """
        filtered = []
        today = datetime.today().date()

        for t in self.transactions:
            t_date = datetime.strptime(t.date, "%Y-%m-%d").date()

            if period == 'today':
                if t_date == today:
                    filtered.append(t)
            elif period == 'week':
                start_of_week = today - timedelta(days=today.weekday())
                if start_of_week <= t_date <= today:
                    filtered.append(t)
            elif period == 'month':
                if t_date.month == today.month and t_date.year == today.year:
                    filtered.append(t)

        return sorted(filtered, reverse=True)


    def calculate_stats(self):
        total_income = 0
        total_expense = 0
        categories = {}

        for t in self.transactions:
            if t.type == 'income':
                total_income += t.amount
            elif t.type == 'expense':
                total_expense += t.amount

                if t.category in categories:
                    categories[t.category] += t.amount
                else:
                    categories[t.category] = t.amount

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            "balance": total_income - total_expense,
            "categories": categories
        }
