# task Створіть клас "Студент" з атрибутами "ім'я", "прізвище",
# "вік" та "середній бал". Створіть об'єкт цього класу, представляючи студента.
# Потім додайте метод до класу "Студент", який дозволяє змінювати середній бал студента.
# Виведіть інформацію про студента та змініть його середній бал.

class Student:
    def __init__(self, name, surname, age, average_grade):
        self.name = name
        self.surname = surname
        self.age = age
        self.average_grade = average_grade

    def change_average_grade(self, new_grade):
        self.average_grade = new_grade


student_1 = Student("Тарас", "Шевченко", 20, 94)

print(
    f"Студент: {student_1.name} {student_1.surname}, "
    f"вік: {student_1.age}, "
    f"середній бал: {student_1.average_grade}"
)

student_1.change_average_grade(98)

print(f"Новий середній бал: {student_1.average_grade}")