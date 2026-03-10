import requests
import pytest
import logging
import os
import sys

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")


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
    session = requests.Session()

    with allure.step("Створити HTTP сесію"):
        logger.info("Створюємо requests.Session()")
        assert session is not None

    with allure.step("Виконати аутентифікацію через /auth"):
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

    with allure.step("Отримати access token з відповіді"):
        data = response.json()
        access_token = data.get("access_token")

        logger.info(f"Access token received: {bool(access_token)}")
        assert access_token, "Токен доступу не отримано"

    with allure.step("Додати Bearer token у headers сесії"):
        session.headers.update({
            "Authorization": f"Bearer {access_token}"
        })

        logger.info("Аутентифікація успішна. Токен додано в Session headers.")
        assert "Authorization" in session.headers

    request.cls.session = session
    yield session

    with allure.step("Закрити HTTP сесію"):
        logger.info("Закриваємо сесію...")
        session.close()


@allure.feature("Search cars API")
@allure.story("Search cars with different query parameters")
@pytest.mark.usefixtures("auth_session")
class TestCarsSearch:

    @allure.title("Перевірка пошуку автомобілів з sort_by={sort_by} і limit={limit}")
    @pytest.mark.parametrize(
        "sort_by, limit",
        [
            ("price", 3),
            ("price", 5),
            ("year", 4),
            ("year", 7),
            ("engine_volume", 3),
            ("brand", 6),
            ("brand", 10),
        ]
    )
    def test_search_cars_with_params(self, sort_by, limit):
        logger.info(f"Запускаємо тест з параметрами: sort_by={sort_by}, limit={limit}")

        with allure.step(f"Відправити GET /cars з sort_by={sort_by} і limit={limit}"):
            response = self.session.get(
                f"{BASE_URL}/cars",
                params={"sort_by": sort_by, "limit": limit}
            )

            logger.info(f"GET /cars status code: {response.status_code}")
            logger.info(f"GET /cars url: {response.url}")

        with allure.step("Перевірити, що статус код відповіді 200"):
            assert response.status_code == 200, (
                f"Очікувався 200, отримано {response.status_code}. "
                f"Body: {response.text}"
            )

        with allure.step("Перетворити відповідь у JSON список автомобілів"):
            cars = response.json()

            logger.info(f"Кількість отриманих записів: {len(cars)}")
            logger.info(f"Отримані дані: {cars}")

            assert isinstance(cars, list), "Відповідь повинна бути списком"

        with allure.step(f"Перевірити, що кількість записів не перевищує limit={limit}"):
            assert len(cars) <= limit, (
                f"Кількість записів {len(cars)} більша за limit={limit}"
            )

        with allure.step("Перевірити наявність обов'язкових полів у кожному автомобілі"):
            for car in cars:
                assert "brand" in car, "Відсутнє поле brand"
                assert "year" in car, "Відсутнє поле year"
                assert "engine_volume" in car, "Відсутнє поле engine_volume"
                assert "price" in car, "Відсутнє поле price"

        with allure.step(f"Перевірити сортування результатів за полем {sort_by}"):
            actual_values = [car[sort_by] for car in cars]
            expected_values = sorted(actual_values)

            logger.info(f"Actual values for {sort_by}: {actual_values}")
            logger.info(f"Expected sorted values: {expected_values}")

            assert actual_values == expected_values, (
                f"Дані не відсортовані по {sort_by}. "
                f"Actual: {actual_values}, Expected: {expected_values}"
            )