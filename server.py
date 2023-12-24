from flask import Flask, request, render_template
import group_schedule
import staff_schedule
import json


app = Flask(__name__, static_folder="static")


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/search")
def search():
    search = request.args.get('search_data', type=str)
    
    with open("jsons/groups.json", encoding='utf-8') as file:
        groups_json = json.load(file)
    with open("jsons/staff.json", encoding='utf-8') as file:
        staff_json = json.load(file)

    found_groups = {}
    for group, id in groups_json.items():
        if search in group:
            found_groups[group] = id

    found_staff = {} 
    for teacher, id in staff_json.items():
        if search in teacher:
            found_staff[teacher] = id

    return render_template('search.html', all_staff=found_staff, all_groups=found_groups)


@app.route("/schedule/groups")
def post_group_schedule():
    id = request.args.get('groupId', type=str)
    week = request.args.get('week', type=int)
    if week is None:
        url = f"https://ssau.ru/rasp?groupId={id}"
    else:
        url = f"https://ssau.ru/rasp?groupId={id}&selectedWeek={str(week)}&selectedWeekday=1"

    group_schedule.parser(url)
    with open("jsons/group_schedule.json", encoding='utf-8') as file:
        schedule = json.load(file)
        return render_template('group_schedule.html', groupId=id, title=schedule['title'], weeks=schedule['weeks'], dates=schedule['dates'], cells=schedule['cells'], length=len(schedule["cells"]))


@app.route("/schedule/staff")
def post_staff_schedule():
    staffId = request.args.get('staffId', type=str)
    week = request.args.get('week', type=int)
    if week is None:
        url = f"https://ssau.ru/rasp?staffId={staffId}"
    else:
        url = f"https://ssau.ru/rasp?staffId={staffId}&selectedWeek={str(week)}&selectedWeekday=1"

    staff_schedule.parser(url)
    with open("jsons/staff_schedule.json", encoding='utf-8') as f:
        schedule = json.load(f)
        return render_template('staff_schedule.html', staffId=staffId, title=schedule['title'], weeks=schedule['weeks'], dates=schedule['dates'], cells=schedule['cells'], length=len(schedule["cells"]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
