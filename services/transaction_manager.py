from services.file_manager import FileManager
from models.transaction import Transaction
from datetime import datetime, timedelta
import csv


class TransactionManager:
    def __init__(self):
        self.file_manager = FileManager()
        self.transactions = self._load_transactions()

    def _load_transactions(self):
        """Вспомогательный метод: читает файл и превращает словари в объекты Transaction"""
        raw_data = self.file_manager.read_data()

        if not isinstance(raw_data, list):
            return []

        return [Transaction.from_dict(item) for item in raw_data]

    def add_transaction(self, transaction):
        self.transactions = self._load_transactions()

        self.transactions.append(transaction)

        data_to_save = [t.to_dict() for t in self.transactions]
        self.file_manager.write_data(data_to_save)

    def get_all_transactions(self):
        self.transactions = self._load_transactions()
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
        self.transactions = self._load_transactions()

        total_income = 0
        total_expense = 0

        income_categories = {}
        expense_categories = {}

        for t in self.transactions:
            if t.type == 'income':
                total_income += t.amount
                if t.category in income_categories:
                    income_categories[t.category] += t.amount
                else:
                    income_categories[t.category] = t.amount
            elif t.type == 'expense':
                total_expense += t.amount
                if t.category in expense_categories:
                    expense_categories[t.category] += t.amount
                else:
                    expense_categories[t.category] = t.amount

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            "balance": total_income - total_expense,
            "income_categories": income_categories,
            "expense_categories": expense_categories
        }

    def export_to_csv(self, filename="data/export.csv"):
        """
        Экспортирует все транзакции в CSV файл, который можно открыть в Excel.
        """
        self.transactions = self._load_transactions()

        fieldnames = ['date', 'type', 'amount', 'category', 'comment']

        try:
            with open(filename, 'w', newline='', encoding="utf-8-sig") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

                writer.writeheader()

                for t in self.transactions:
                    writer.writerow({
                        "date": t.date,
                        "type": t.type,
                        "category": t.category,
                        "amount": t.amount,
                        "comment": t.comment if t.comment else ""
                    })
            return True, filename
        except Exception as e:
            return False, str(e)
