from flask import Flask, render_template, request, redirect, jsonify
from Job import Jobs
from Update_mongo import JobWheelUpdate

app = Flask(__name__)
# data = Jobs("JS Job Wheel", "./credentials.json")
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
    google_doc = Jobs("JS Job Wheel", "./credentials.json")
    updater = JobWheelUpdate().insert(google_doc.get_full_dict())
    return redirect("/")


@app.route("/_get_data")
def get_data():
    member_name = request.args.get("name", type=str)
    data = JobWheelUpdate().retrieve()["Assigned jobs"][member_name]
    return jsonify(result=data)


if __name__ == "__main__":
    app.run(debug=True)
