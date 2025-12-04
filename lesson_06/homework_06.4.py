# Є ліст з числами, порахуйте сумму усіх ПАРНИХ чисел в цьому лісті

# numbers = [1, 5, 6, 1, 9, 3, 3, 6, 4, 8, 9, 3, 5, 9, 8, 1, 6, 3, 5, 8, 9]

numbers = list(map(int, input("Введіть числа через пробіл: ").split()))

total = sum(i for i in numbers if i % 2 == 0)
print(total)