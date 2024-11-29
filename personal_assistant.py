from datetime import datetime
import json


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
                now = datetime.now()
                timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
                title = input('Введите название заметки: ')
                content = input('Введите текст: ')
                Note(title, content, timestamp).create_note()
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
    def __init__(self, title, content, timestamp):
        self.title = title
        self.content = content
        self.timestamp = timestamp

    def create_note(self):
        #Достаем id следующей заметки
        try:
            with open('notes.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.id = int(data[-1]['id']) + 1
        except FileNotFoundError:
            data = []
            self.id = 1

        #Грузим новую заметку в notes.json
        new_note = {'id': self.id,
                    'title': self.title,
                    'content': self.content,
                    'timestamp': self.timestamp}
        data.append(new_note)

        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print('Заметка успешно добавлена в файл notes.json\n')

###Тесты
greetings = GreetPage()
greetings.tool_bars()
