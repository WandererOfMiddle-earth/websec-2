import html
import json
import re


def parser(url):
    data = {}
    raw = re.sub("\n", " ", html.get_html(url))

    name = re.findall(r"<h1 class=\"h1-text page-header\">(.*?)<\/h1>", raw)
    data["name"] = name[0].strip()

    data["courses"] = []
    courses = re.findall(r"(\d курс)", raw)
    for i in range(1, len(courses)+1):
        string = " " + str(i) + " курс "
        data["courses"].append(string)

    info = {}

    qualifications = re.findall(r"<h2 class=\"h2-text group-catalog__edtype\">(.*?)<\/h2>", raw)
    info["qualifications"] = []
    for element in qualifications:
        info["qualifications"].append(element.strip())

    info["education_forms"] = []
    info["groups"] = []
    education_forms_and_groups = re.findall(r"<div class=\"card-default group-catalog__item\">(.*?)<\/div><\/div>", raw)
    for element in education_forms_and_groups:
        education_forms = re.findall(r"<h3 class=\"h3-text group-catalog__edform\">(.*?)<\/h3>", element)
        
        groups = []
        for elem in element.split("><h3"):
            gr = re.findall(r"<span>(.*?)<\/span>", elem)
            groups.append(gr)
        for i in range(len(education_forms)):
            education_forms[i] = education_forms[i].strip()

        info["education_forms"].append(education_forms)
        info["groups"].append(groups)

    file = open("jsons/groups.json", encoding="utf-8")
    groups_json = json.load(file)

    full_structure = []
    for qualification, education_forms, all_groups in zip(info["qualifications"], info["education_forms"], info["groups"]):
        pairs = []
        for education_form, groups in zip(education_forms, all_groups):
            groups_and_ids = []
            for group in groups:
                groups_and_ids.append({group : groups_json[group]})
            pairs.append([education_form, groups_and_ids])
        full_structure.append({qualification : pairs})
    data["qualifications"] = full_structure

    with open("jsons/faculty_groups.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)