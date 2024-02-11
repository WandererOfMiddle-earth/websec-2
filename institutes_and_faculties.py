import html
import json
import re


def parser():
    institutes_and_faculties = {}

    raw = re.sub("\n", " ", html.get_html("https://ssau.ru/rasp"))

    lines = re.findall(r"<div class=\"card-default faculties__item\">(.*?)<\/div>", raw)
    for line in lines:
        data = re.findall(r"<a href=\"/rasp/faculty/(.*?)\?course=1\" class=\"h3-text\"> (.*?) <\/a>", line)
        name = data[0][1]
        id = data[0][0]
        institutes_and_faculties[name] = id

    del institutes_and_faculties["Институт дополнительного образования"]

    with open("jsons/institutes_and_faculties.json", "w", encoding="utf-8") as file:
        json.dump(institutes_and_faculties, file, indent=4, ensure_ascii=False, sort_keys=True)