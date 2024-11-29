from datetime import datetime
import json
from pprint import pprint


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
                now = datetime.now()
                self.timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
                self.title = input('Введите название заметки: ')
                self.content = input('Введите текст: ')

                self.create_note(self.title, self.content, self.timestamp)
            elif choice == "2":
                self.viewing_notes()
            elif choice == "3":
                pass
            elif choice == "4":
                pass
            elif choice == "5":
                pass
            elif choice == "6":
                pass
            elif choice == "7":
                print("Cumback\n")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 7.")


    def create_note(self, title, content, timestamp):
        #Достаем id следующей заметки
        try:
            with open('notes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except Exception as e:
            print(f'Произошла неведомая ошибка {e}')
            return

        if data:
            id = int(data[-1].get('id', 1)) + 1
        else:
            id = 1
            
        #Добавляем новую заметку к data
        new_note = {'id': id,
                    'title': title,
                    'content': content,
                    'timestamp': timestamp}
        data.append(new_note)

        #Грузим заметки в notes.json
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print('Заметка успешно добавлена в файл notes.json\n')


    def viewing_notes(self):
        try:
            with open('notes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        pprint(data)



###Тесты
greetings = GreetPage()
greetings.tool_bars()
