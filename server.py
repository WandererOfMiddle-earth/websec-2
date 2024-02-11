from flask import Flask, request, render_template
import groups
import staff
import institutes_and_faculties
import faculty_groups
import group_schedule
import staff_schedule
import json
import os


app = Flask(__name__, static_folder="static")


@app.route("/")
@app.route("/institutes_and_faculties")
def post_institutes_and_faculties():
    if not os.path.exists("jsons/groups.json"):
        groups.parser()
    if not os.path.exists("jsons/staff.json"):
        staff.parser()
    if not os.path.exists("jsons/institutes_and_faculties.json"):
        institutes_and_faculties.parser()

    with open("jsons/institutes_and_faculties.json", encoding="utf-8") as file:
        IaF = json.load(file) # IaF = Institutes and Faculties
        return render_template("institutes_and_faculties.html", 
                               institutes_and_faculties = IaF)


@app.route("/search")
def search():
    search = request.args.get("search_data", type=str)
    
    with open("jsons/groups.json", encoding="utf-8") as file:
        groups_json = json.load(file)
    with open("jsons/staff.json", encoding="utf-8") as file:
        staff_json = json.load(file)

    found_groups = {}
    for group, id in groups_json.items():
        if search in group:
            found_groups[group] = id

    found_staff = {} 
    for teacher, id in staff_json.items():
        if search in teacher:
            found_staff[teacher] = id

    return render_template("search.html", 
                           all_staff=found_staff, 
                           all_groups=found_groups)


@app.route("/faculty")
def post_faculty_groups():
    id = request.args.get("facultyId", type=str)
    course = request.args.get("course", type=str)
    url = f"https://ssau.ru/rasp/faculty/{id}?course={course}"
    
    faculty_groups.parser(url)
    with open("jsons/faculty_groups.json", encoding="utf-8") as file:
        FG = json.load(file) # FG = faculty groups

        for i in range(len(FG["courses"])):
            if str(course) == FG["courses"][i][1]:
                FG["courses"][i] = "[" + FG["courses"][i][1:-1] + "]"
        
        return render_template("faculty_groups.html", 
                               facultyId=id, 
                               name=FG["name"], 
                               courses=FG["courses"], 
                               courses_length=100//len(FG["courses"]), 
                               qualifications=FG["qualifications"])


@app.route("/schedule/group")
def post_group_schedule():
    id = request.args.get("groupId", type=str)
    week = request.args.get("week", type=str)
    if week is None:
        url = f"https://ssau.ru/rasp?groupId={id}"
    else:
        url = f"https://ssau.ru/rasp?groupId={id}&selectedWeek={week}&selectedWeekday=1"

    group_schedule.parser(url)
    with open("jsons/group_schedule.json", encoding="utf-8") as file:
        schedule = json.load(file)
        return render_template("group_schedule.html", 
                               groupId=id, 
                               title=schedule["title"], 
                               weeks=schedule["weeks"], 
                               dates=schedule["dates"], 
                               cells=schedule["cells"], 
                               length=len(schedule["cells"]))


@app.route("/schedule/staff")
def post_staff_schedule():
    id = request.args.get("staffId", type=str)
    week = request.args.get("week", type=str)
    if week is None:
        url = f"https://ssau.ru/rasp?staffId={id}"
    else:
        url = f"https://ssau.ru/rasp?staffId={id}&selectedWeek={week}&selectedWeekday=1"

    staff_schedule.parser(url)
    with open("jsons/staff_schedule.json", encoding="utf-8") as f:
        schedule = json.load(f)

        staff_name = schedule["title"].split(" ")
        small_staff_name = staff_name[0] + " "
        for i in range(1, len(staff_name)):
            small_staff_name += staff_name[i][0] + ". "
        small_staff_name = small_staff_name[:-1]

        return render_template("staff_schedule.html", 
                               staffId=id, 
                               title=schedule["title"], 
                               small_title=small_staff_name, 
                               weeks=schedule["weeks"], 
                               dates=schedule["dates"], 
                               cells=schedule["cells"], 
                               length=len(schedule["cells"]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
