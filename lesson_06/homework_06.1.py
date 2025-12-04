# Порахувати кількість унікальних символів в строці.
# Якщо їх більше 10 - вивести в консоль True, інакше - False.
# Строку отримати за допомогою функції input()

string = input("Введіть запит: ")

set_string = set(string)

print(("Кількість унікальних значень ="), len(set_string))

if len(set_string) > 10:
    print(True)
else:
    print(False)

