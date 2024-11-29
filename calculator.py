class Calculator:
    def calc(self):
        print("\nКалькулятор:")
        while True:
            try:
                expression = input("Введите выражение для вычисления (или 'exit' для выхода): ")
                if expression.lower() == "exit":
                    break
                result = eval(expression)
                print(f"Результат: {result}")
            except ZeroDivisionError:
                print("Ошибка: деление на ноль!")
            except Exception as e:
                print(f"Ошибка: {e}")