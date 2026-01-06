# task 1
""" Задача - надрукувати табличку множення на задане число, але
лише до максимального значення для добутку - 25.
Код майже готовий, треба знайти помилки та виправити\доповнити.
"""
def multiplication_table(number):
    # Initialize the appropriate variable
    multiplier = 1

    # Complete the while loop condition.
    while multiplier != 0:
        result = number * multiplier
        # десь тут помила, а може не одна
        if  result >= 25:
            break
        print(str(number) + "x" + str(multiplier) + "=" + str(result))

        # Increment the appropriate variable
        multiplier += 1


multiplication_table(3)
# Should print:
# 3x1=3
# 3x2=6
# 3x3=9
# 3x4=12
# 3x5=15


# task 2
"""  Написати функцію, яка обчислює суму двох чисел.
"""
def sum_two_numbers(a, b):
    return a + b

print(sum_two_numbers(3, 2))


# task 3
"""  Написати функцію, яка розрахує середнє арифметичне списку чисел.
"""
lst = [1, 1, 7]
mt_lst = []

def average(some_lst):
    if not some_lst:
        return 0
    return sum(some_lst) / len(some_lst)

print(average(lst))
print(average(mt_lst))


# task 4
"""  Написати функцію, яка приймає рядок та повертає його у зворотному порядку.
"""
string = "Рядок"

def reverse_string(text):
    return text[::-1]

print(reverse_string(string))


# task 5
"""  Написати функцію, яка приймає список слів та повертає найдовше слово у списку.
"""
words = ['cat', 'Gibraltar', 'apple']

def longest_word(some_lst):
    if not some_lst:
        return None
    longest = some_lst[0]
    for word in some_lst:
        if len(word) > len(longest):
            longest = word

    return longest

print(longest_word(words))


# task 6
"""  Написати функцію, яка приймає два рядки та повертає індекс першого входження другого рядка
у перший рядок, якщо другий рядок є підрядком першого рядка, та -1, якщо другий рядок
не є підрядком першого рядка."""

def find_substring(str1, str2):
    return str1.find(str2)

str1 = "Hello, world!"
str2 = "world"
print(find_substring(str1, str2)) # поверне 7

str1 = "The quick brown fox jumps over the lazy dog"
str2 = "cat"
print(find_substring(str1, str2)) # поверне -1


# task 7
# Площа Чорного моря становить 436 402 км2, а площа Азовського
# моря становить 37 800 км2. Яку площу займають Чорне та Азовське моря разом?

def total_sea_area(black_sea, azov_sea):
    return black_sea + azov_sea
black_sea_area = 436_402
azov_sea_area = 37_800

result = total_sea_area(black_sea_area, azov_sea_area)
print(result)


# task 8
# Мережа супермаркетів має 3 склади, де всього розміщено
# 375 291 товар. На першому та другому складах перебуває
# 250 449 товарів. На другому та третьому – 222 950 товарів.
# Знайдіть кількість товарів, що розміщені на кожному складі.

def warehouse_items(total, first_second, second_third):
    third = total - first_second
    second = second_third - third
    first = first_second - second
    return first, second, third

result = warehouse_items(
    total = 375_291,
    first_second = 250_449,
    second_third = 222_950
)
print(result)


# task 9
# Михайло разом з батьками вирішили купити комп’ютер, ско-
# риставшись послугою «Оплата частинами». Відомо, що сплачу-
# вати необхідно буде півтора року по 1179 грн/місяць. Обчисліть
# вартість комп’ютера.

def computer_price(monthly_payment, years):
    months = years * 12
    return months * monthly_payment
price = computer_price(1179, 1.5)
print(price)


# task 10
# Ігор займається фотографією. Він вирішив зібрати всі свої 232
# фотографії та вклеїти в альбом. На одній сторінці може бути
# розміщено щонайбільше 8 фото. Скільки сторінок знадобиться
# Ігорю, щоб вклеїти всі фото?

def album_pages(photos, photos_per_page):
    return (photos + photos_per_page - 1) // photos_per_page
pages = album_pages(232, 8)
print(pages)


"""  Оберіть будь-які 4 таски з попередніх домашніх робіт та
перетворіть їх у 4 функції, що отримують значення та повертають результат.
Обоязково документуйте функції та дайте зрозумілі імена змінним.
"""