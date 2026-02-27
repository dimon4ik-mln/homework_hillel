# У venv Python встановiть Flask за допомогою команди pip install flask
# Створiть у окремiй директорiї файл app.py та скопiюйте у нього код файлу app.py який приведено нижче в початкових даних.
# Запустiть http сервер за допомогою команди python app.py
# Сервер стартує за базовою адресою http://127.0.0.1:8080
# Враховуючи документацiю яку наведено нижче вам потрiбно написати код який використовуючи модуль request
# зробить через POST upload якогось зображення на сервер, за допомогою GET отримає посилання на цей файл и
# потiм за допомогою DELETE зробить видалення файлу з сервера

import os
from urllib.parse import urlparse, quote

import requests

BASE_URL = "http://127.0.0.1:8080"


def upload_image(image_path: str) -> str:
    """
    POST /upload
    Надсилаємо файл як multipart/form-data з полем 'image'
    Повертає image_url з відповіді.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл не знайдено: {image_path}")

    with open(image_path, "rb") as f:
        files = {
            "image": (os.path.basename(image_path), f, "image/jpeg")
        }
        r = requests.post(f"{BASE_URL}/upload", files=files, timeout=20)
        r.raise_for_status()

    data = r.json()
    image_url = data["image_url"]
    return image_url


def extract_filename(image_url: str) -> str:
    """
    З image_url типу http://127.0.0.1:8080/uploads/example.jpg
    дістаємо 'example.jpg'
    """
    path = urlparse(image_url).path  # /uploads/example.jpg
    filename = path.rsplit("/", 1)[-1]
    if not filename:
        raise ValueError(f"Не вдалося витягнути filename з URL: {image_url}")
    return filename


def get_image_url(filename: str) -> str:
    """
    GET /image/<filename>
    За умовою: якщо Content-Type = text -> повертає JSON з image_url
    """
    encoded = quote(filename)  # важливо для ULR encoding
    headers = {"Content-Type": "text"}  # за їхньою логікою з ТЗ
    r = requests.get(f"{BASE_URL}/image/{encoded}", headers=headers, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data["image_url"]


def delete_image(filename: str) -> dict:
    """
    DELETE /delete/<filename>
    Повертає JSON-повідомлення сервера.
    """
    encoded = quote(filename)
    r = requests.delete(f"{BASE_URL}/delete/{encoded}", timeout=20)
    r.raise_for_status()
    return r.json()


def main():
    image_path = "test.jpg"

    image_url_from_upload = upload_image(image_path)
    print("UPLOAD OK, image_url:", image_url_from_upload)

    filename = extract_filename(image_url_from_upload)
    print("FILENAME:", filename)

    image_url_from_get = get_image_url(filename)
    print("GET OK, image_url:", image_url_from_get)

    delete_resp = delete_image(filename)
    print("DELETE OK, response:", delete_resp)


if __name__ == "__main__":
    main()