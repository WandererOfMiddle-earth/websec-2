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
                data['cells'].append({ "count": 0 })
            elif element[0] != "":
                data["cells"].append({ "time" : [element[0], element[1]] })
            elif element[3] != "":
                elems = re.findall(r"schedule__discipline.*?\">(.*?)<\/div>|schedule__place\">(.*?)<\/div>|schedule__teacher\">.*?([а-яА-Яё][^<>]+[а-яА-Яё\.])|schedule__groups\">.*?(\d{4}-\d{6}D.*?\d{4}-\d{6}D|[а-яА-Яё][^<>]+[а-яА-Яё\.^0-9])", element[3])
                lesson = {}
                lesson["count"] = 0
                lesson["name"] = []
                lesson["place"] = []
                lesson["teacher"] = []
                lesson["group"] = []
                for elem in elems:
                    if elem[0] != "":
                        lesson["name"].append(elem[0].strip())
                    elif elem[1] != "":
                        lesson["place"].append(elem[1].strip())
                    elif elem[2] != "":
                        lesson["teacher"].append(elem[2].strip())
                    elif elem[3] != "":
                        if len(elem[3]) > 30:
                            groups = re.findall(r"\d{4}-\d{6}D", elem[3])
                            res = ""
                            for group in groups:
                                res += group + "\n"
                            lesson["group"].append(res.strip())
                        else:
                            lesson["group"].append(elem[3])
                lesson["count"] = len(lesson["name"])
                data["cells"].append(lesson)

    with open("jsons/group_schedule.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)