from pprint import pprint
import json
import csv

class Contacts:
    def __init__(self):
        self.id = None
        self.name = None
        self.phone = None
        self.email = None

    # Функция управления контактами
    def managing_contacts(self):
        while True:
            print('Управление контактами:')
            print('1. Добавить новый контакт \n'
                  '2. Поиск контакта \n'
                  '3. Редактировать контакт \n'
                  '4. Удалить контакт\n'
                  '5. Экспорт контакта в CSV\n'
                  '6. Импорт контакта из CSV\n'
                  '7. Назад\n')

            choice = input('Выберите действие: ')

            if choice == "1":
                self.name = input('Введите имя: ')
                self.phone = input('Введите номер телефона (11 цифр, начиная с 8): ')
                self.email = input('Введите почту: ')
                self.create_contact(self.name, self.phone, self.email)
                
            elif choice == "2":
                self.name = input('Введите имя: ')
                self.email = input('Введите почту: ')
                self.search_contact(self.name, self.email)

            elif choice == "3":
                self.id = str(input('Введите id интересующего контакта: '))
                self.name = input('Введите имя: ')
                self.phone = input('Введите номер телефона (11 цифр, начиная с 8): ')
                self.email = input('Введите почту: ')
                self.editing_contact(self.id, self.name, self.phone, self.email)
                
            elif choice == "4":
                self.id = str(input('Введите id интересующего контакта: '))
                self.delete_contact(self.id)
                
            elif choice == "5":
                self.json_to_csv()
            elif choice == "6":
                self.csv_to_json()
            elif choice == "7":
                print("Cumback\n")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 8")

    # Функция создания контакта
    def create_contact(self, name, phone, email):
        # Достаем id следующего контакта
        data = self.read_contacts()

        if data:
            id = int(data[-1].get('id', 1)) + 1
        else:
            id = 1

        # Добавляем новую задачу к data
        new_contact = {'id': str(id),
                       'name': name,
                       'phone': phone,
                       'email': email}
        data.append(new_contact)

        # Грузим задачу в tasks.json
        self.upload_contacts(data)

    # Функция поиска контакта
    def search_contact(self, name, email):
        data = self.read_contacts()
        f = False
        for contact in data:
            if contact['name'].lower() == name.lower() or contact['email'].lower() == email.lower():
                print(f"О дааа, мы нашли покемона, его id '{contact['id']}'")
                f = True
                break
        if not f:
            print('Покемон не нашелся(')

    # Редактирование контакта
    def editing_contact(self, id, name, phone, email):
        data = self.read_contacts()
        data_of_id = [elem['id'] for elem in data]
        if id in data_of_id:
            new_contact = {'id': str(id),
                           'name': name,
                           'phone': phone,
                           'email': email}
            data.append(new_contact)
            self.upload_contacts(data)
        else:
            print('Ячейки с таким id не существует')

    # Удаление контакта
    def delete_contact(self, id):
        data = self.read_contacts()
        data_of_id = [elem['id'] for elem in data]
        if id in data_of_id:
            data.pop(data_of_id.index(id))
            self.upload_contacts(data)
        else:
            print('Ячейки с таким id не существует')

    def json_to_csv(self, json_file='contacts.json', csv_file='contacts_export.csv'):
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

    def csv_to_json(self, json_file='contacts.json', csv_file='contacts_export.csv'):
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

    # Отдельная функция чтения контактов
    def read_contacts(self):
        try:
            with open('contacts.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    # Отдельная функция загрузки контактов в файл contacts.json
    def upload_contacts(self, data):
        with open('contacts.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
