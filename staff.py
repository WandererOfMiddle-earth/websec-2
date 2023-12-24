from tqdm import tqdm
import html
import json
import re


staff = {}

raw = re.sub("\n", " ", html.get_html("https://ssau.ru/staff"))
page_max = max(list(map(lambda x: int(x), re.findall(r"(?<=page=)\d+", raw))))

for page in tqdm(range(page_max), desc="Creating staff.json file"):
    raw = re.sub("\n", " ", html.get_html(f"https://ssau.ru/staff?page={page+1}&letter=0"))
    lines = re.findall(r"https:\/\/ssau\.ru\/staff\/\d+.*?(?=<\/a>)", raw)

    for line in lines:
        line = re.sub(r"-.*>", "", line)
        line = re.sub(r".*\/", "", line)
        data = line.strip().split(" ", 1)
        staff[data[1]] = data[0]

with open("jsons/staff.json", "w", encoding="utf-8") as file:
    json.dump(staff, file, indent=4, ensure_ascii=False, sort_keys=True)
