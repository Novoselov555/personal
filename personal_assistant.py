from datetime import datetime
import json
from pprint import pprint

from wheel.macosx_libfile import read_data


class GreetPage:
    def tool_bars(self):
        while True:
            print('Добро пожаловать в Персональный помощник!')
            print('Выберите действие:')
            print('1. Управление заметками \n'
                  '2. Управление задачами \n'
                  '3. Управление контактами \n'
                  '4. Управление финансовыми записями\n'
                  '5. Калькулятор\n'
                  '6. Выход\n')

            choice = input('Выберите действие: ')

            if choice == "1":
                Note().managing_notes()
            elif choice == "2":
                pass
            elif choice == "3":
                pass
            elif choice == "4":
                pass
            elif choice == "5":
                pass
            elif choice == "6":
                print("Выход из приложения. До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 6.")


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
                  '6. Импорт и экспорт заметок в формате CSV\n'
                  '7. Назад\n')

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
                self.id = int(input('Введите id интересующей вас заметки: '))
                self.title = input('Введите название заметки: ')
                self.content = input('Введите текст: ')
                self.timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.editing_note(self.id, self.title, self.content, self.timestamp)
            elif choice == "5":
                pass
            elif choice == "6":
                pass
            elif choice == "7":
                print("Cumback\n")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 7.")

    # Функция создания заметок
    def create_note(self, title, content, timestamp):
        # Достаем id следующей заметки
        data = self.read_notes()

        if data:
            id = int(data[-1].get('id', 1)) + 1
        else:
            id = 1

        # Добавляем новую заметку к data
        new_note = {'id': id,
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
        id = int(input('Введите id интересующей вас заметки: '))
        if len(data) < id or id < 1:
            print('Ячейки с таким id не существует')
        else:
            pprint(data[id - 1])

    # Редактирование заметки
    def editing_note(self, id, title, content, timestamp):
        data = self.read_notes()
        if 1 <= id <= len(data):
            new_note = {'id': id,
                        'title': title,
                        'content': content,
                        'timestamp': timestamp}
            data[id - 1] = new_note
            self.upload_notes(data)
        else:
            print('Ячейки с таким id не существует')

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
        print('Заметка успешно добавлена в файл notes.json\n')


###Тесты
greetings = GreetPage()
greetings.tool_bars()
