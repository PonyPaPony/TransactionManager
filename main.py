from datetime import datetime
from models.transaction import Transaction
from services.transaction_manager import TransactionManager
from utils.validators import Validators


class ConsoleApp:
    def __init__(self):
        self.manager = TransactionManager()
        self.validators = Validators()


    def _get_menu_choice(self, options: dict):
        """
        Универсальный метод выбора из меню.
        options: словарь вида {'1': 'Описание 1', '2': 'Описание 2'},
        возвращает ключ, который выбрал пользователь.
        """
        while True:
            for key, description in options.items():
                print(f"{key}. {description}")

            choice = input("Выберите действие: ").strip()

            if choice in options:
                return choice

            print("❌ Неверный выбор, попробуйте снова.\n")

    def run(self):
        menu_options = {
            "1": "Добавить доход",
            "2": "Добавить расход",
            "3": "Просмотр транзакций",
            "4": "Статистика",
            "5": "Экспорт в CSV",
            "6": "Выход"
        }
        while True:
            print("\n--- Финансовый менеджер ---")
            choice = self._get_menu_choice(menu_options)

            try:
                if choice == "1":
                    self.process_transaction("income")
                elif choice == "2":
                    self.process_transaction("expense")
                elif choice == "3":
                    self.review_menu()
                elif choice == "4":
                    self.calculate_menu()
                elif choice == "5":
                    print("⏳ Экспорт данных...")
                    self.export_csv()
                    input("\nНажмите Enter, чтобы продолжить...")
                elif choice == "6":
                    print("Всего доброго!")
                    break
            except Exception as e:
                print(f"Произошла ошибка: {e}")

    def export_csv(self):
        success, message = self.manager.export_to_csv()

        if success:
            print(f"✅ Данные успешно выгружены в файл: {message}")
            print("Теперь вы можете открыть этот файл в Excel.")
        else:
            print(f"❌ Ошибка при экспорте: {message}")

    def review_menu(self):
        print("\n--- Меню просмотра ---")
        filter_options = {
            "1": "Все транзакции",
            "2": "За сегодня",
            "3": "За эту неделю",
            "4": "За этот месяц",
            "5": "Назад"
        }

        choice = self._get_menu_choice(filter_options)
        if choice == "5":
            return

        transactions = []
        if choice == "1":
            transactions = self.manager.get_all_transactions()
        elif choice == "2":
            transactions = self.manager.get_filtered_transactions("today")
        elif choice == "3":
            transactions = self.manager.get_filtered_transactions("week")
        elif choice == "4":
            transactions = self.manager.get_filtered_transactions("month")

        print("\n📄 Отчет:")
        if not transactions:
            print("Записей не найдено.")
        else:
            for tx in transactions:
                print(tx)

        input("\nНажмите Enter, чтобы продолжить...")

    def calculate_menu(self):
        stats = self.manager.calculate_stats()
        print("\n--- Статистика ---")
        print(f"📈 Общий доход:  {stats['total_income']:,.2f}".replace(",", " "))
        print(f"📉 Общий расход: {stats['total_expense']:,.2f}".replace(",", " "))
        print(f"💰 Баланс:       {stats['balance']:,.2f}".replace(",", " "))

        print("\n📊 Доходы по категориям:")
        if not stats['income_categories']:
            print(" - Нет данных")
        else:
            for cat, summ in stats['income_categories'].items():
                print(f" - {cat}: {summ:,.2f}".replace(",", " "))

        print("\n📊 Расходы по категориям:")
        if not stats['expense_categories']:
            print(" - Нет данных")
        else:
            for cat, summ in stats['expense_categories'].items():
                print(f" - {cat}: {summ:,.2f}".replace(",", " "))

        # Тоже добавим паузу
        input("\nНажмите Enter, чтобы вернуться в меню...")

    def process_transaction(self, t_type):
        while True:
            print(f"\n--- Добавление: {t_type} ---")
            print("(Введите 'q' или 'отмена' в любой момент для возврата в меню)")

            # Убираем общий try, чтобы обрабатывать этапы точечно

            # 1. Ввод СУММЫ
            while True:
                amount_str = input("Введите сумму: ").strip()
                if amount_str.lower() in ['q', 'cancel', 'отмена']:
                    print("🔙 Ввод отменен.")
                    return

                try:
                    amount = float(amount_str)
                    # Проверка бизнес-правил (сумма > 0)
                    Validators.check_amount(amount)
                    break  # Если всё ок - идем дальше
                except ValueError:
                    # Этот блок поймает и ошибку конвертации float, и ошибку от Validators
                    print("❌ Ошибка: Введите корректное положительное число.")

            # 2. Ввод КАТЕГОРИИ
            while True:
                category = input("Укажите категорию: ").strip()
                if category.lower() in ['q', 'отмена', 'cancel']:
                    print("🔙 Ввод отменен.")
                    return

                if category:
                    break
                print("❌ Категория не может быть пустой")

            # 3. Ввод ДАТЫ
            while True:
                dt_input = input("Введите дату (YYYY-MM-DD) или Enter для сегодня: ").strip()
                if dt_input.lower() in ['q', 'отмена', 'cancel']:
                    print("🔙 Ввод отменен.")
                    return

                if not dt_input or dt_input == "0":
                    date_str = datetime.now().strftime("%Y-%m-%d")
                else:
                    date_str = dt_input

                # Проверяем дату валидатором
                is_valid, error_msg = Validators.check_date(date_str)

                if not is_valid:
                    print(f"❌ Ошибка: {error_msg}")
                    continue

            # 4. Ввод КОММЕНТАРИЯ
            comment = input("Комментарий: ").strip()
            if comment.lower() in ['q', 'отмена', 'cancel']:
                print("🔙 Ввод отменен.")
                return

            if not comment:
                comment = None

            # 5. СОЗДАНИЕ ТРАНЗАКЦИИ
            try:
                # Тут снова сработают проверки внутри Transaction (на всякий случай)
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
                    break  # Выходим в главное меню

            except ValueError as e:
                print(f"❌ Системная ошибка валидации: {e}")

if __name__ == '__main__':
    app = ConsoleApp()
    app.run()