# Оберіть від 3 до 5 різних домашніх завдань
# перетворюєте їх у функції (якщо це потрібно)
# створіть в папці файл homeworks.py куди вставте ваші функції з дз
# та покрийте їх не менш ніж 10 тестами (це загальна к-сть на все ДЗ).

class Rhombus:
    def __init__(self, side_a, angle_a):
        self.side_a = side_a
        self.angle_a = angle_a

    def __setattr__(self, name, value):
        if name == "side_a":
            if value <= 0:
                raise ValueError("Довжина сторони повинна бути більше 0")

        if name == "angle_a":
            if not (0 < value < 180):
                raise ValueError("Кут A повинен бути в межах 0–180 градусів")

            object.__setattr__(self, "angle_b", 180 - value)

        object.__setattr__(self, name, value)

if __name__ == "__main__":
    rhombus = Rhombus(20, 80)
    print("Сторона a:", rhombus.side_a)
    print("Кут A:", rhombus.angle_a)
    print("Кут B:", rhombus.angle_b)



def sum_numbers(text):
    try:
        numbers = text.split(",")
        total = 0

        for num in numbers:
            total += int(num)

        return total

    except ValueError:
        return "Не можу це зробити!"

data = ["1,2,3,4", "1,2,3,4,50", "qwerty1,2,3"]

for item in data:
    print(sum_numbers(item))

