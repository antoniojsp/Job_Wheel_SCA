from pprint import pprint
from flask import Flask, render_template, redirect, jsonify
from Job import JobsSchedule
from Update import JobWheelUpdate
app = Flask(__name__)
data = JobWheelUpdate().retrieve()


@app.route("/")
def index():
    titles = data["Current term name"]
    return render_template('index.html',
                           title=titles)


@app.route("/update")
def update_job_wheel():
    """
    google_sheet gets all the data from Google Sheets and transform it into a dictionary
    to be stored by JobWheelUpdate().insert() in MongoDB
    """
    google_sheet = JobsSchedule(sheet_title="JS Job Wheel")
    JobWheelUpdate().insert(google_sheet.get_full_dict())
    return redirect("/")


@app.route("/_get_dictionary")
def get_dictionary():
    """
    send json from flask to the js client.
    JS
    :return:
    """
    job_wheel_info = JobWheelUpdate().retrieve()
    return jsonify(result=job_wheel_info)


if __name__ == "__main__":
    app.run(debug=True)
