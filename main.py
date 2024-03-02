from pprint import pprint

from flask import Flask, render_template, request, redirect, jsonify
from Job import Jobs
from Update_mongo import JobWheelUpdate

app = Flask(__name__)
data = JobWheelUpdate().retrieve()


@app.route("/")
def index():
    names = data["Members names"]
    titles = data["Current term name"]
    names = sorted(names)

    return render_template('index.html',
                           title=titles,
                           names=names)


@app.route("/update")
def update_job_wheel():
    google_sheet = Jobs("JS Job Wheel", "./credentials.json")
    updater = JobWheelUpdate().insert(google_sheet.get_full_dict())
    return redirect("/")


@app.route("/_get_data")
def get_data():
    member_name = request.args.get("name", type=str)
    job_wheel_info = data["Assigned jobs"]
    return jsonify(result=job_wheel_info[member_name])


@app.route("/_get_dictionary")
def get_dictonary():
    job_wheel_info = dict(data)
    del job_wheel_info['_id']
    return jsonify(result=job_wheel_info)


if __name__ == "__main__":
    app.run(debug=True)
