#Генератори:
# Напишіть генератор, який повертає послідовність парних чисел від 0 до N.
# Створіть генератор, який генерує послідовність Фібоначчі до певного числа N.

# Парні числа
def even_numbers(n):
    yield from range(0, n+1, 2)
for number in even_numbers(10):
    print(number)


# Фібоначчі
def fibonacci(n):
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b
for number in fibonacci(50):
    print(number)


#Ітератори:
# Реалізуйте ітератор для зворотного виведення елементів списку.
# Напишіть ітератор, який повертає всі парні числа в діапазоні від 0 до N

#Ітератор для зворотного виведення списку
class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration

        value = self.data[self.index]
        self.index -= 1
        return value


numbers = [1, 2, 3, 4, 5]

for item in ReverseIterator(numbers):
    print(item)

#Ітератор парних чисел від 0 до N
class EvenIterator:
    def __init__(self, n):
        self.n = n
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self.current > self.n:
            raise StopIteration

        value = self.current
        self.current += 2

        return value

for number in EvenIterator(10):
    print(number)


#Декоратори:
# Напишіть декоратор, який логує аргументи та результати викликаної функції.
# Створіть декоратор, який перехоплює та обробляє винятки, які виникають в ході виконання функції.

#Декоратор, який логує аргументи і результат функції

def log_decorator(func):

    def wrapper(*args, **kwargs):
        print("Аргументи:", args, kwargs)

        result = func(*args, **kwargs)

        print("Результат:", result)

        return result

    return wrapper


@log_decorator
def add(a, b):
    return a + b

add(3, 5)


#Декоратор перехоплення винятків

def exception_handler(func):

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            print("Сталася помилка:", e)

    return wrapper


@exception_handler
def divide(a, b):
    return a / b

divide(10, 2)
divide(10, 0)