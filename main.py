from flask import Flask, render_template, request, redirect, jsonify
from Job import Jobs
from Update_mongo import JobWheelUpdate
app = Flask(__name__)
data = Jobs("JS Job Wheel", "./credentials.json")


@app.route("/")
def index():
    titles = data.get_sheet_names()
    titles[0] += " (Current term)"
    names = ["------------"] + data.get_members_names()
    return render_template('index.html', title=titles[0], titles=titles, names=names)


@app.route("/update")
def update_job_wheel():
    google_doc = Jobs("JS Job Wheel", "./credentials.json")
    updater = JobWheelUpdate().insert(google_doc.get_full_dict())
    return redirect("/")

@app.route("/_get_data")
def get_data():
    member_name = request.args.get("name", type=str)
    data = JobWheelUpdate().retrieve()[member_name]
    return jsonify(result=data)

if __name__ == "__main__":
    app.run(debug=True)
