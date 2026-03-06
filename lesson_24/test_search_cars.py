import logging
import sys

import pytest
import requests
from requests.auth import HTTPBasicAuth


BASE_URL = "http://127.0.0.1:8080"


def setup_logger():
    logger = logging.getLogger("cars_search_tests")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler("test_search.log", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()


@pytest.fixture(scope="class")
def auth_session(request):
    """
    Фікстура класового рівня:
    - створює requests.Session()
    - проходить первинну аутентифікацію
    - додає Bearer token в headers для всієї сесії
    """
    session = requests.Session()

    logger.info("Починаємо аутентифікацію користувача...")

    response = session.post(
        f"{BASE_URL}/auth",
        auth=HTTPBasicAuth("test_user", "test_pass")
    )

    logger.info(f"Auth status code: {response.status_code}")
    logger.info(f"Auth response: {response.text}")

    assert response.status_code == 200, (
        f"Помилка аутентифікації. "
        f"Status code: {response.status_code}, body: {response.text}"
    )

    data = response.json()
    access_token = data.get("access_token")

    assert access_token, "Токен доступу не отримано"

    session.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    logger.info("Аутентифікація успішна. Токен додано в Session headers.")

    request.cls.session = session
    yield session

    logger.info("Закриваємо сесію...")
    session.close()


@pytest.mark.usefixtures("auth_session")
class TestCarsSearch:

    @pytest.mark.parametrize(
        "sort_by, limit",
        [
            ("price", 3),
            ("price", 10),
            ("year", 5),
            ("year", 8),
            ("engine_volume", 4),
            ("brand", 7),
            ("brand", 12),
        ]
    )
    def test_search_cars_with_params(self, sort_by, limit):
        logger.info(f"Запускаємо тест з параметрами: sort_by={sort_by}, limit={limit}")

        response = self.session.get(
            f"{BASE_URL}/cars",
            params={"sort_by": sort_by, "limit": limit}
        )

        logger.info(f"GET /cars status code: {response.status_code}")
        logger.info(f"GET /cars url: {response.url}")

        assert response.status_code == 200, (
            f"Очікувався 200, отримано {response.status_code}. "
            f"Body: {response.text}"
        )

        cars = response.json()

        logger.info(f"Кількість отриманих записів: {len(cars)}")
        logger.info(f"Отримані дані: {cars}")

        assert isinstance(cars, list), "Відповідь повинна бути списком"
        assert len(cars) <= limit, (
            f"Кількість записів {len(cars)} більша за limit={limit}"
        )

        for car in cars:
            assert "brand" in car
            assert "year" in car
            assert "engine_volume" in car
            assert "price" in car

        actual_values = [car[sort_by] for car in cars]
        expected_values = sorted(actual_values)

        assert actual_values == expected_values, (
            f"Дані не відсортовані по {sort_by}. "
            f"Actual: {actual_values}, Expected: {expected_values}"
        )

        logger.info(
            f"Тест пройдено успішно для параметрів: sort_by={sort_by}, limit={limit}"
        )