from flask import Flask, render_template, redirect, jsonify
from update import JobWheelUpdate
from member_jobs import MemberJobs
from gather_cells import GatherCells
app = Flask(__name__)

current_raw_data = GatherCells(title="JS Job Wheel").get_cells_data()

@app.route("/")
def index():
    titles = current_raw_data[0]
    return render_template('index.html',
                           title=titles)


@app.route("/update")
def update_job_wheel():
    """
    google_sheet gets all the data from Google Sheets and transform it into a dictionary
    to be stored by JobWheelUpdate().insert() in MongoDB
    """
    cells = GatherCells(title="JS Job Wheel").get_cells_data()
    google_sheet = MemberJobs(cells)
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
