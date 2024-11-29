from notes import Notes
from tasks import Tasks
from contacts import Contacts
from calculator import Calculator
from finance_manager import FinanceRecord

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
                Notes().managing_notes()
            elif choice == "2":
                Tasks().managing_tasks()
            elif choice == "3":
                Contacts().managing_contacts()
            elif choice == "4":
                FinanceRecord().manage_records()
            elif choice == "5":
                Calculator().calc()
            elif choice == "6":
                print("Выход из приложения. До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите номер от 1 до 6")


greetings = GreetPage()
greetings.tool_bars()
