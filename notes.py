from datetime import datetime
from pprint import pprint
import json
import csv

class Note:
    def __init__(self):
        self.id = None
        self.title = None
        self.content = None
        self.timestamp = None

    # Функция управления заметками
    def managing_notes(self):
        while True:
            print('Управление заметками:')
            print('1. Создание новой заметки \n'
                  '2. Просмотр списка заметок \n'
                  '3. Просмотр подробностей заметки \n'
                  '4. Редактирование заметки\n'
                  '5. Удаление заметки\n'
                  '6. Экспорт заметок в CSV\n'
                  '7. Импорт заметок из CSV\n'
                  '8. Назад\n')

            choice = input('Выберите действие: ')

            if choice == "1":
                self.title = input('Введите название заметки: ')
                self.content = input('Введите текст: ')
                self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.create_note(self.title, self.content, self.timestamp)
            elif choice == "2":
                self.viewing_notes()
            elif choice == "3":
                self.view_note_details()
            elif choice == "4":
                self.id = str(input('Введите id интересующей вас заметки: '))
                self.title = input('Введите название заметки: ')
                self.content = input('Введите текст: ')
                self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.editing_note(self.id, self.title, self.content, self.timestamp)
            elif choice == "5":
                self.id = str(input('Введите id интересующей вас заметки: '))
                self.delete_note(self.id)
            elif choice == "6":
                self.json_to_csv()
            elif choice == "7":
                self.csv_to_json()
            elif choice == "8":
                print("Cumback\n")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 8")

    # Функция создания заметок
    def create_note(self, title, content, timestamp):
        # Достаем id следующей заметки
        data = self.read_notes()

        if data:
            id = int(data[-1].get('id', 1)) + 1
        else:
            id = 1

        # Добавляем новую заметку к data
        new_note = {'id': str(id),
                    'title': title,
                    'content': content,
                    'timestamp': timestamp}
        data.append(new_note)

        # Грузим заметки в notes.json
        self.upload_notes(data)

    # Функция просмотра заметок
    def viewing_notes(self):
        data = self.read_notes()
        pprint(data)

    # Я не понял, че значит "Просмотр подробностей заметки", поэтому просто вывожу инфу о конкретной заметке
    def view_note_details(self):
        data = self.read_notes()
        data_of_id = [elem['id'] for elem in data]
        id = str(input('Введите id интересующей вас заметки: '))
        if id not in data_of_id:
            print('Ячейки с таким id не существует')
        else:
            pprint(data[data_of_id.index(id)])

    # Редактирование заметки
    def editing_note(self, id, title, content, timestamp):
        data = self.read_notes()
        data_of_id = [elem['id'] for elem in data]
        if id in data_of_id:
            new_note = {'id': id,
                        'title': title,
                        'content': content,
                        'timestamp': timestamp}
            data[data_of_id.index(id)] = new_note
            self.upload_notes(data)
        else:
            print('Ячейки с таким id не существует')

    # Удаление заметки
    def delete_note(self, id):
        data = self.read_notes()
        data_of_id = [elem['id'] for elem in data]
        if id in data_of_id:
            data.pop(data_of_id.index(id))
            self.upload_notes(data)
        else:
            print('Ячейки с таким id не существует')

    def json_to_csv(self, json_file='notes.json', csv_file='notes_export.csv'):
        try:
            # Читаем данные из JSON файла
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Проверяем, есть ли данные для экспорта
            if not data:
                print("JSON файл пуст. Нечего экспортировать.")
                return

            # Открываем CSV файл для записи
            with open(csv_file, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Данные успешно экспортированы из {json_file} в {csv_file}.")

        except FileNotFoundError:
            print(f"Файл {json_file} не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON в файле {json_file}.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def csv_to_json(self, json_file='notes.json', csv_file='notes_export.csv'):
        try:
            # Читаем данные из CSV файла
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]

            # Записываем данные в JSON файл
            with open(json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print(f"Данные успешно импортированы из {csv_file} в {json_file}.")

        except FileNotFoundError:
            print(f"Файл {csv_file} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    # Отдельная функция чтения заметок
    def read_notes(self):
        try:
            with open('notes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    # Отдельная функция загрузки заметок в файл notes.json
    def upload_notes(self, data):
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
