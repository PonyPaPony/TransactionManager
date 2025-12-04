from datetime import datetime
from models.transaction import Transaction
from services.transaction_manager import TransactionManager
from utils.validators import Validators


class ConsoleApp:
    def __init__(self):
        self.manager = TransactionManager()
        self.validators = Validators()

    def run(self):
        while True:
            try:
                print("\n--- Финансовый менеджер ---")
                print("1. Добавить доход")
                print("2. Добавить расход")
                print("3. Просмотр")
                print("4. Расчет дохода/расхода")
                print("5. Выход")

                choice = input("Выберите действие: ").strip()

                if choice == "1":
                    self.process_transaction("income")
                elif choice == "2":
                    self.process_transaction("expense")
                elif choice == "3":
                    print("\n1. Все транзакции")
                    print("2. За сегодня")
                    print("3. За эту неделю")
                    print("4. За этот месяц")
                    filter_choice = input("Выберите фильтр: ")

                    transactions = []
                    if filter_choice == "1":
                        transactions = self.manager.get_all_transactions()
                    elif filter_choice == "2":
                        transactions = self.manager.get_filtered_transactions("today")
                    elif filter_choice == "3":
                        transactions = self.manager.get_filtered_transactions("week")
                    elif filter_choice == "4":
                        transactions = self.manager.get_filtered_transactions("month")

                    print("--Финансовый отчет--")
                    if not transactions:
                        print("Записей не найдено.")
                    for tx in transactions:
                        print(tx)
                elif choice == "4":
                    stats = self.manager.calculate_stats()
                    print("\n--- Статистика ---")
                    print(f"Общий доход: {stats['total_income']}")
                    print(f"Общий расход: {stats['total_expense']}")
                    print(f"Баланс: {stats['balance']}")
                    print("Расходы по категориям:")
                    for cat, summ in stats['categories'].items():
                        print(f" - {cat}: {summ}")
                elif choice == "5":
                    print("Всего доброго!")
                    break
                else:
                    print("Неверный выбор, попробуйте снова.")
            except ValueError:
                print("Ошибка ввода.")

    def process_transaction(self, t_type):
        while True:
            print(f"\n--- Добавление: {t_type} ---")
            try:
                amount_str = input("Введите сумму: ")
                amount = float(amount_str)
                self.validators.check_amount(amount)

                category = input("Укажите категорию: ").strip()
                if not category:
                    print("Категория не может быть пустой")
                    continue

                dt_input = input("Введите дату (YYYY-MM-DD) или Enter для сегодня: ").strip()
                if not dt_input or dt_input == "0":
                    date_str = datetime.now().strftime("%Y-%m-%d")
                else:
                    date_str = dt_input
                    if not self.validators.check_date(date_str):
                        print("Неверный формат даты!")
                        continue

                comment = input("Комментарий: ").strip()
                if not comment:
                    comment = None

                tx = Transaction(
                    t_type=t_type,
                    amount=amount,
                    category=category,
                    date=date_str,
                    comment=comment
                )

                self.manager.add_transaction(tx)
                print("✅ Запись успешно сохранена!")

                retry = input("Добавить еще? (y/n): ").lower()
                if retry != "y":
                    break

            except ValueError:
                print("❌ Ошибка: Введите корректное число для суммы.")

    def print_all_transactions(self):
        print("--Финансовый отчет--")
        for tx in self.manager.get_all_transactions():
            print(tx)

if __name__ == '__main__':
    app = ConsoleApp()
    app.run()