from __future__ import annotations

import random
from typing import Iterable

from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    select,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
    selectinload,
)


# -------------------------
# DB + Base
# -------------------------
DB_URL = "sqlite:///students.db"
engine = create_engine(DB_URL, echo=False)  # постав echo=True якщо хочеш бачити SQL
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


# -------------------------
# Association table (many-to-many)
# -------------------------
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
)


# -------------------------
# Models
# -------------------------
class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)

    courses: Mapped[list["Course"]] = relationship(
        secondary=student_course,
        back_populates="students",
    )

    def __repr__(self) -> str:
        return f"Student(id={self.id}, full_name={self.full_name!r})"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    students: Mapped[list[Student]] = relationship(
        secondary=student_course,
        back_populates="courses",
    )

    def __repr__(self) -> str:
        return f"Course(id={self.id}, title={self.title!r})"


# -------------------------
# Helpers / CRUD
# -------------------------
def create_tables() -> None:
    Base.metadata.create_all(engine)


def seed_data() -> None:
    """Створює 5 курсів і 20 студентів, розподіляє студентів випадково по 1..3 курси.
    Повторний запуск не дублює (якщо в БД вже є дані).
    """
    course_titles = ["Python", "QA Automation", "Databases", "Web", "Algorithms"]

    first_names = ["Ivan", "Olena", "Dmytro", "Sofiia", "Andrii", "Yulia", "Mykola", "Iryna"]
    last_names = ["Shevchenko", "Koval", "Melnyk", "Bondarenko", "Tkachenko", "Kravchenko"]

    with SessionLocal() as session:
        existing_courses = session.scalar(select(Course.id))
        existing_students = session.scalar(select(Student.id))
        if existing_courses or existing_students:
            print("Seed пропущено: дані вже є в БД.")
            return

        courses = [Course(title=title) for title in course_titles]
        session.add_all(courses)
        session.flush()

        students: list[Student] = []
        for _ in range(20):
            full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            s = Student(full_name=full_name)

            s.courses = random.sample(courses, k=random.randint(1, 3))
            students.append(s)

        session.add_all(students)
        session.commit()

    print("Seed виконано: 5 курсів та 20 студентів створено.")


def add_student_and_enroll(full_name: str, course_title: str) -> Student:
    """Додає студента та записує на курс."""
    with SessionLocal() as session:
        course = session.scalar(select(Course).where(Course.title == course_title))
        if not course:
            raise ValueError(f"Course {course_title!r} not found")

        student = Student(full_name=full_name)
        student.courses.append(course)

        session.add(student)
        session.commit()
        session.refresh(student)
        return student


def get_students_by_course(course_title: str) -> list[Student]:
    with SessionLocal() as session:
        stmt = (
            select(Student)
            .join(student_course)      # join через association table
            .join(Course)              # join до courses
            .where(Course.title == course_title)
            .options(selectinload(Student.courses))  # <-- ключова строка
            .distinct()
        )
        return list(session.scalars(stmt).all())


def get_courses_by_student(student_id: int) -> list[Course]:
    with SessionLocal() as session:
        student = session.get(
            Student,
            student_id,
            options=[selectinload(Student.courses)]
        )
        if not student:
            return []
        return list(student.courses)


def update_student_name(student_id: int, new_full_name: str) -> bool:
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        if not student:
            return False
        student.full_name = new_full_name
        session.commit()
        return True


def update_course_title(course_id: int, new_title: str) -> bool:
    with SessionLocal() as session:
        course = session.get(Course, course_id)
        if not course:
            return False
        course.title = new_title
        session.commit()
        return True


def remove_student(student_id: int) -> bool:
    """Видаляє студента (і автоматично прибирає зв’язки у student_course)."""
    with SessionLocal() as session:
        student = session.get(Student, student_id)
        if not student:
            return False
        session.delete(student)
        session.commit()
        return True


def print_students(students: Iterable[Student]) -> None:
    for s in students:
        course_titles = [c.title for c in s.courses]
        print(f"- {s.id}: {s.full_name} | courses={course_titles}")


def print_courses(courses: Iterable[Course]) -> None:
    for c in courses:
        print(f"- {c.id}: {c.title}")


# -------------------------
# Demo сценарій
# -------------------------
def main() -> None:
    create_tables()
    seed_data()

    # 1) Додати нового студента і записати на курс
    new_student = add_student_and_enroll("Dmytro Melnychenko", "Python")
    print(f"\nДодано студента: {new_student}")

    # 2) Запит: студенти на певному курсі
    python_students = get_students_by_course("Python")
    print("\nСтуденти на курсі Python:")
    print_students(python_students)

    # 3) Запит: курси конкретного студента
    courses_of_new = get_courses_by_student(new_student.id)
    print(f"\nКурси студента id={new_student.id}:")
    print_courses(courses_of_new)

    # 4) Оновлення даних
    ok = update_student_name(new_student.id, "Dmytro M. (updated)")
    print(f"\nОновлення імені студента: {'OK' if ok else 'NOT FOUND'}")

    # 5) Видалення
    ok = remove_student(new_student.id)
    print(f"Видалення студента: {'OK' if ok else 'NOT FOUND'}")


if __name__ == "__main__":
    main()