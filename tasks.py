from pprint import pprint
import json
import csv

class Tasks:
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.done = None
        self.priority = None
        self.due_date = None

    # Функция управления задачами
    def managing_tasks(self):
        while True:
            print('Управление задачами:')
            print('1. Добавить новую задачу \n'
                  '2. Просмотреть задачи \n'
                  '3. Отметить задачу как выполненную \n'
                  '4. Редактировать задачу\n'
                  '5. Удалить задачу\n'
                  '6. Экспорт задач в CSV\n'
                  '7. Импорт задач из CSV\n'
                  '8. Назад\n')

            choice = input('Выберите действие: ')

            if choice == "1":
                self.title = input('Введите название задачи: ')
                self.description = input('Введите описание задачи: ')
                self.done = False
                self.priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
                self.due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
                self.create_task(self.title, self.description, self.done, self.priority, self.due_date)
            elif choice == "2":
                self.viewing_tasks()
            elif choice == "3":
                self.done_task()
            elif choice == "4":
                self.id = str(input('Введите id интересующей вас задачи: '))
                self.title = input('Введите название задачи: ')
                self.description = input('Введите описание задачи: ')
                self.done = False
                self.priority = input('Выберите приоритет (Высокий/Средний/Низкий): ')
                self.due_date = input('Введите срок выполнения (в формате ДД-ММ-ГГГГ): ')
                self.editing_task(self.id, self.title, self.description, self.done, self.priority, self.due_date)
            elif choice == "5":
                self.id = str(input('Введите id интересующей вас задачи: '))
                self.delete_task(self.id)
            elif choice == "6":
                self.json_to_csv()
            elif choice == "7":
                self.csv_to_json()
            elif choice == "8":
                print("Cumback\n")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 8")

    # Функция создания задач
    def create_task(self, title, description, done, priority, due_date):
        # Достаем id следующей задачи
        data = self.read_tasks()

        if data:
            id = int(data[-1].get('id', 1)) + 1
        else:
            id = 1

        # Добавляем новую задачу к data
        new_task = {'id': str(id),
                    'title': title,
                    'description': description,
                    'done': done,
                    'priority': priority,
                    'due_date': due_date}
        data.append(new_task)

        # Грузим задачу в tasks.json
        self.upload_tasks(data)

    # Функция просмотра задач
    def viewing_tasks(self):
        data = self.read_tasks()
        pprint(data)

    # Смена статуса задачи
    def done_task(self):
        data = self.read_tasks()
        data_of_id = [elem['id'] for elem in data]
        id = str(input('Введите id интересующей вас задачи: '))
        task_status = input('Задача закрыта(да/нет): ')
        if id not in data_of_id:
            print('Ячейки с таким id не существует')
        else:
            if task_status.lower() == 'да':
                data[data_of_id.index(id)]['done'] = True
                print(f"Задача '{data[data_of_id.index(id)]['title']}' выполнена")
            elif task_status.lower() == 'нет':
                data[data_of_id.index(id)]['done'] = False
                print(f"Задача '{data[data_of_id.index(id)]['title']}' не выполнена")
            else:
                print('За баловство получаешь невыполненную задачу')
                data[data_of_id.index(id)]['done'] = False

    # Редактирование задачи
    def editing_task(self, id, title, description, done, priority, due_date):
        data = self.read_tasks()
        data_of_id = [elem['id'] for elem in data]
        if id in data_of_id:
            new_task = {'id': str(id),
                        'title': title,
                        'description': description,
                        'done': done,
                        'priority': priority,
                        'due_date': due_date}
            data.append(new_task)
            self.upload_tasks(data)
        else:
            print('Ячейки с таким id не существует')

    # Удаление задачи
    def delete_task(self, id):
        data = self.read_tasks()
        data_of_id = [elem['id'] for elem in data]
        if id in data_of_id:
            data.pop(data_of_id.index(id))
            self.upload_tasks(data)
        else:
            print('Ячейки с таким id не существует')

    def json_to_csv(self, json_file='tasks.json', csv_file='tasks_export.csv'):
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

    def csv_to_json(self, json_file='tasks.json', csv_file='tasks_export.csv'):
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
    def read_tasks(self):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    # Отдельная функция загрузки заметок в файл notes.json
    def upload_tasks(self, data):
        with open('tasks_export.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
