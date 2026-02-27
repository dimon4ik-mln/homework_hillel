# Є відкритий офіційний API NASA Images and Video Library ( https://images-api.nasa.gov ),
# який дозволяє виконувати пошук медіа та отримувати список файлів (assets) для кожного знайденого медіа-елемента.
# Ваше завдання - за допомогою модуля requests:
# 1. Виконати пошук зображень, пов’язаних з ровером Curiosity на Марсі.
# 2. З JSON відповіді витягнути nasa_id для знайдених елементів.
# 3. Для кожного nasa_id зробити додатковий запит до endpoint-а /asset/{nasa_id}, щоб отримати список URL-ів файлів.
# 4. Обрати з цього списку посилання на JPG-зображення (наприклад, перший .jpg або “найкращий” варіант, якщо їх кілька).
# 5. Скачати 2 зображення і зберегти локально як:
# mars_photo1.jpg
# mars_photo2.jpg
# Важливо: потрібно виконати мінімум 3 HTTP-запити:
# 1 запит /search + 2 запити /asset/{nasa_id} (і ще 2 запити на скачування jpg-файлів).
# Доступні endpoint-и (Images API)
# GET /search?q={q} - пошук медіа
# GET /asset/{nasa_id} - список файлів (URL) для вибраного медіа

import os
import requests
from typing import List, Optional

BASE_URL = "https://images-api.nasa.gov"

HEADERS = {
    "User-Agent": "python-requests (NASA images homework)"
}

TIMEOUT = 20


def search_nasa_ids(query: str, page_size: int = 20) -> List[str]:
    """GET /search -> витягуємо nasa_id з collection.items[].data[0].nasa_id"""
    url = f"{BASE_URL}/search"
    params = {
        "q": query,
        "media_type": "image",
        "page_size": page_size,
    }

    resp = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("collection", {}).get("items", [])
    nasa_ids = []
    for item in items:
        data_arr = item.get("data", [])
        if not data_arr:
            continue
        nasa_id = data_arr[0].get("nasa_id")
        if nasa_id:
            nasa_ids.append(nasa_id)

    seen = set()
    unique_ids = []
    for nid in nasa_ids:
        if nid not in seen:
            seen.add(nid)
            unique_ids.append(nid)

    return unique_ids


def get_asset_urls(nasa_id: str) -> List[str]:
    """GET /asset/{nasa_id} -> повертає список URL-ів (collection.items[].href)"""
    url = f"{BASE_URL}/asset/{nasa_id}"

    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("collection", {}).get("items", [])
    hrefs = []
    for it in items:
        href = it.get("href")
        if isinstance(href, str):
            hrefs.append(href)

    return hrefs


def pick_best_jpg(urls: List[str]) -> Optional[str]:
    """
    Обираємо 'найкращий' JPG без додаткових запитів:
    - беремо лише .jpg/.jpeg
    - віддаємо пріоритет назвам з 'orig' / 'large' / 'medium'
    (у NASA assets часто є кілька розмірів + метадані .json)
    """
    jpgs = [u for u in urls if u.lower().endswith((".jpg", ".jpeg"))]
    if not jpgs:
        return None

    def score(u: str) -> int:
        s = u.lower()
        if "orig" in s or "original" in s:
            return 300
        if "large" in s:
            return 200
        if "medium" in s:
            return 100
        return 10

    return sorted(jpgs, key=score, reverse=True)[0]


def download_file(url: str, out_path: str) -> None:
    """Скачуємо файл стрімінгом, щоб не тримати все в RAM."""
    with requests.get(url, headers=HEADERS, stream=True, timeout=TIMEOUT) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 64):
                if chunk:
                    f.write(chunk)


def main():
    nasa_ids = search_nasa_ids("Curiosity rover Mars", page_size=20)
    if len(nasa_ids) < 2:
        raise RuntimeError("Знайдено менше 2 nasa_id — спробуй інший запит або збільш page_size.")

    chosen_ids = nasa_ids[:2]

    saved_files = ["mars_photo1.jpg", "mars_photo2.jpg"]

    for nasa_id, out_name in zip(chosen_ids, saved_files):
        asset_urls = get_asset_urls(nasa_id)

        jpg_url = pick_best_jpg(asset_urls)
        if not jpg_url:
            raise RuntimeError(f"Для nasa_id={nasa_id} не знайдено JPG у /asset відповіді.")

        download_file(jpg_url, out_name)
        print(f"OK: {out_name} <- {jpg_url}")

    print("\nГотово! Збережені файли:")
    for f in saved_files:
        print(" -", os.path.abspath(f))


if __name__ == "__main__":
    main()