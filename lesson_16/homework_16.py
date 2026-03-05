# Завдання 1:
#Візміть два файли з теки ideas_for_test/work_with_csv порівняйте на наявність дублікатів і приберіть їх.
# Результат запишіть у файл result_<your_second_name>.csv

import csv

files = ["random-michaels.csv", "r-m-c.csv"]

rows = set()

for file in files:
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.update(tuple(row) for row in reader)

with open("result_Shevchenko.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)


# Завдання 2:
# Провалідуйте, чи усі файли у папці ideas_for_test/work_with_json є валідними json.
# результат для невалідного файлу виведіть через логер на рівні еррор у файл json__<your_second_name>.log

import json
import logging

logging.basicConfig(
    filename='json_Shevchenko.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

files = [
    "swagger.json",
    "login.json",
    "localizations_en.json",
    "localizations_ru.json"
]

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            json.load(f)

        print(f"{file} → валідний JSON")

    except json.JSONDecodeError as e:
        logging.error(f"{file} → невалідний JSON: {e}")
        print(f"{file} → НЕвалідний JSON")


# Завдання 3:
# Для файла ideas_for_test/work_with_xml/groups.xml створіть функцію пошуку по group/number і
# повернення значення timingExbytes/incoming результат виведіть у консоль через логер на рівні інфо

import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO)


def get_incoming(group_number):

    tree = ET.parse("groups.xml")
    root = tree.getroot()

    for group in root.findall("group"):

        if group.find("number").text == str(group_number):

            incoming = group.find("timingExbytes/incoming").text

            logging.info(f"Group {group_number} incoming = {incoming}")
            return incoming

    logging.info("Group not found")
    return None


get_incoming(2)