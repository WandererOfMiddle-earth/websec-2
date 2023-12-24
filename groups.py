from tqdm import tqdm
import html
import json
import re


groups = {}

raw = re.sub("\n", " ", html.get_html("https://ssau.ru/rasp"))
lines = re.findall(r"<a href=\"\/rasp\/faculty\/\d+\?course=1\" class=\"h3-text\">.*?<\/a>", raw)

for line in tqdm(lines, desc="Creating groups.json file"):
    IaF_id = re.findall(r"\d+(?=\?)", line)[0] # IaF = Institutes and Faculties
    raw = html.get_html(f"https://ssau.ru/rasp/faculty/{IaF_id}")
    years = list(map(lambda x: int(x), re.findall(r"(?<=course=)\d+", raw)))

    for year in years:
        raw = html.get_html(f"https://ssau.ru/rasp/faculty/{IaF_id}?course={year}")
        another_lines = re.findall(r"(?<=groupId=).*\d{4}-\d{6}D", raw)

        for another_line in another_lines:
            data = re.sub(r"\".*(?=\d{4}-\d{6}D)", " ", another_line).split()
            groups[data[1]] = data[0]

with open("jsons/groups.json", "w", encoding="utf-8") as file:
        json.dump(groups, file, indent=4, ensure_ascii=False, sort_keys=True)