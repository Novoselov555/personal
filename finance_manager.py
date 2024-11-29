from datetime import datetime
from pprint import pprint
import json
import csv

class FinanceRecord:
    def __init__(self):
        self.id = None
        self.amount = None
        self.category = None
        self.date = None
        self.description = None

    # Управление финансовыми записями
    def manage_records(self):
        while True:
            print('Управление финансовыми записями:')
            print('1. Добавить новую запись\n'
                  '2. Просмотреть все записи\n'
                  '3. Генерация отчёта\n'
                  '4. Удалить запись\n'
                  '5. Экспорт финансовых записей в CSV\n'
                  '6. Импорт финансовых записей из CSV\n'
                  '7. Назад\n')

            choice = input('Выберите действие: ')

            if choice == "1":
                self.amount = float(input('Введите сумму (положительное число для доходов, отрицательное для расходов): '))
                self.category = input('Введите категорию: ')
                self.date = input('Введите дату (ДД-ММ-ГГГГ): ')
                self.description = input('Введите описание: ')
                self.add_record(self.amount, self.category, self.date, self.description)
            elif choice == "2":
                self.view_records()
            elif choice == "3":
                start_date = input('Введите начальную дату (ДД-ММ-ГГГГ): ')
                end_date = input('Введите конечную дату (ДД-ММ-ГГГГ): ')
                self.generate_report(start_date, end_date)
            elif choice == "4":
                self.id = input('Введите ID записи для удаления: ')
                self.delete_record(self.id)
            elif choice == "5":
                self.json_to_csv()
            elif choice == "6":
                self.csv_to_json()
            elif choice == "7":
                print("Возврат в главное меню.\n")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 7.")

    # Добавление новой записи
    def add_record(self, amount, category, date, description):
        data = self.read_records()

        if data:
            new_id = str(int(data[-1]['id']) + 1)
        else:
            new_id = "1"

        new_record = {
            'id': new_id,
            'amount': amount,
            'category': category,
            'date': date,
            'description': description
        }
        data.append(new_record)
        self.upload_records(data)
        print("Запись успешно добавлена.")

    # Просмотр всех записей
    def view_records(self):
        data = self.read_records()
        if data:
            pprint(data)
        else:
            print("Записи отсутствуют.")

    # Генерация отчёта
    def generate_report(self, start_date, end_date):
        data = self.read_records()
        start = datetime.strptime(start_date, "%d-%m-%Y")
        end = datetime.strptime(end_date, "%d-%m-%Y")
        filtered = [record for record in data if start <= datetime.strptime(record['date'], "%d-%m-%Y") <= end]

        # Расчёт доходов, расходов и баланса
        income = sum(record['amount'] for record in filtered if record['amount'] > 0)
        expenses = sum(record['amount'] for record in filtered if record['amount'] < 0)
        balance = income + expenses

        # Форматирование отчёта
        print(f"Финансовый отчёт за период с {start_date} по {end_date}:")
        print(f" - Общий доход: {income:.2f} руб.")
        print(f" - Общие расходы: {abs(expenses):.2f} руб.")
        print(f" - Баланс: {balance:.2f} руб.")

        # Сохранение подробной информации в CSV
        report_file = f"report_{start_date}_{end_date}.csv"
        try:
            with open(report_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "amount", "category", "date", "description"])
                writer.writeheader()
                writer.writerows(filtered)
            print(f"Подробная информация сохранена в файле {report_file}")
        except Exception as e:
            print(f"Ошибка при сохранении отчёта: {e}")

    # Удаление записи
    def delete_record(self, record_id):
        data = self.read_records()
        ids = [record['id'] for record in data]
        if record_id in ids:
            data.pop(ids.index(record_id))
            self.upload_records(data)
            print(f"Запись с ID {record_id} успешно удалена.")
        else:
            print("Записи с таким ID не существует.")

    # Экспорт записей в CSV
    def json_to_csv(self, json_file='finance.json', csv_file='finance_export.csv'):
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not data:
                print("JSON файл пуст. Нечего экспортировать.")
                return

            with open(csv_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Данные успешно экспортированы из {json_file} в {csv_file}.")

        except FileNotFoundError:
            print(f"Файл {json_file} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    # Импорт записей из CSV
    def csv_to_json(self, json_file='finance.json', csv_file='finance_export.csv'):
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]

            for record in data:
                record['amount'] = float(record['amount'])  # Преобразование суммы в float

            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Данные успешно импортированы из {csv_file} в {json_file}.")

        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    # Чтение записей из JSON
    def read_records(self):
        try:
            with open('finance.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    # Сохранение записей в JSON
    def upload_records(self, data):
        with open('finance.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
