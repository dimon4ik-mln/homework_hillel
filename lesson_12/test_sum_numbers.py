# Оберіть від 3 до 5 різних домашніх завдань
# перетворюєте їх у функції (якщо це потрібно)
# створіть в папці файл homeworks.py куди вставте ваші функції з дз
# та покрийте їх не менш ніж 10 тестами (це загальна к-сть на все ДЗ).

import unittest
from lesson_12.homework_12 import sum_numbers

class TestSumNumbers(unittest.TestCase):

    def test_simple_case(self):
        self.assertEqual(sum_numbers("1,2,3,4"), 10)

    def test_big_number(self):
        self.assertEqual(sum_numbers("1,2,3,4,50"), 60)

    def test_text_should_fail(self):
        self.assertEqual(sum_numbers("qwerty1,2,3"), "Не можу це зробити!")

    def test_single_number(self):
        self.assertEqual(sum_numbers("7"), 7)

    def test_negative_numbers(self):
        self.assertEqual(sum_numbers("-1,-2"), -3)

    def test_spaces(self):
        self.assertEqual(sum_numbers(" 1, 2, 3 "), 6)

    def test_zero(self):
        self.assertEqual(sum_numbers("0,0,0"), 0)

    def test_trailing_comma(self):
        self.assertEqual(sum_numbers("1,2,"), "Не можу це зробити!")

    def test_double_comma(self):
        self.assertEqual(sum_numbers("1,,2"), "Не можу це зробити!")

    def test_empty_string(self):
        self.assertEqual(sum_numbers(""), "Не можу це зробити!")


if __name__ == "__main__":
    unittest.main()