import html
import json
import re


def parser(url):
    data = {}
    raw = re.sub("\n", " ", html.get_html(url))

    title = re.search(r"<h2 class=\"h2-text info-block__title\">(.*?)<\/h2>", raw)
    data['title'] = title.group(1).strip()

    weeks = re.findall(r"(\d{1,2}) неделя", raw)
    data['weeks'] = weeks

    dates = re.findall(r"schedule__head-date.*?(\d{2}\.\d{2}\.\d{4})", raw)
    data['dates'] = dates
    
    data['cells'] = []
    raw = re.findall(r"\"schedule__time\".*?(\d\d:\d\d).*?(\d\d:\d\d)|\"schedule__item (schedule__item_show|)\"><\/div>|\"schedule__lesson(.*?)<\/div><\/div><\/div>", raw)
    if (len(raw) != 0):
        for element in raw:
            if element[0] == "" and element[3] == "":
                data['cells'].append([])
            elif element[0] != "":
                data["cells"].append({ "time" : [element[0], element[1]] })
            elif element[3] != "":
                elems = re.findall(r"schedule__discipline.*?\">(.*?)<\/div>|schedule__place\">(.*?)<\/div>|schedule__group\">(.*?)<\/a>", element[3])
                lesson = {}
                lesson["name"] = ""
                lesson["place"] = ""
                lesson["group"] = ""
                for elem in elems:
                    if elem[0] != "":
                        lesson["name"] = elem[0].strip()
                    elif elem[1] != "":
                        lesson["place"] = elem[1].strip()
                    elif elem[2] != "":
                        lesson["group"] = elem[2].strip()
                data["cells"].append(lesson)

    with open("jsons/staff_schedule.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)