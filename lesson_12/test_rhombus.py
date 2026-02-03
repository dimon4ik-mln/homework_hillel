# Оберіть від 3 до 5 різних домашніх завдань
# перетворюєте їх у функції (якщо це потрібно)
# створіть в папці файл homeworks.py куди вставте ваші функції з дз
# та покрийте їх не менш ніж 10 тестами (це загальна к-сть на все ДЗ).

import unittest
from lesson_12.homework_12 import Rhombus

class TestRhombus(unittest.TestCase):

    def test_create_valid_rhombus(self):
        r = Rhombus(10, 60)
        self.assertEqual(r.side_a, 10)
        self.assertEqual(r.angle_a, 60)
        self.assertEqual(r.angle_b, 120)

    def test_angle_b_calculated_correctly(self):
        r = Rhombus(5, 45)
        self.assertEqual(r.angle_b, 135)

    def test_change_angle_a_updates_angle_b(self):
        r = Rhombus(10, 30)
        r.angle_a = 70
        self.assertEqual(r.angle_b, 110)

    def test_side_a_cannot_be_zero(self):
        with self.assertRaises(ValueError):
            Rhombus(0, 60)

    def test_side_a_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            Rhombus(-5, 60)

    def test_angle_a_cannot_be_zero(self):
        with self.assertRaises(ValueError):
            Rhombus(10, 0)

    def test_angle_a_cannot_be_180(self):
        with self.assertRaises(ValueError):
            Rhombus(10, 180)

    def test_angle_a_cannot_be_more_than_180(self):
        with self.assertRaises(ValueError):
            Rhombus(10, 200)

    def test_angle_a_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            Rhombus(10, -30)

    def test_change_side_a_valid(self):
        r = Rhombus(10, 60)
        r.side_a = 20
        self.assertEqual(r.side_a, 20)

    def test_change_side_a_invalid(self):
        r = Rhombus(10, 60)
        with self.assertRaises(ValueError):
            r.side_a = -10

    def test_angle_b_always_sum_180(self):
        r = Rhombus(15, 20)
        self.assertEqual(r.angle_a + r.angle_b, 180)


if __name__ == "__main__":
    unittest.main()