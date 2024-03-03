from flask import Flask, render_template, redirect, jsonify
from update import JobWheelUpdate
from member_jobs import MemberJobs
from gather_cells import GatherCells

app = Flask(__name__)

current_raw_data = JobWheelUpdate().retrieve()

@app.route("/")
def index():
    return render_template('index.html',
                           title=current_raw_data['Current term name'])


@app.route("/update")
def update_job_wheel():
    """
    google_sheet gets all the data from Google Sheets and transform it into a dictionary
    to be stored by JobWheelUpdate().insert() in MongoDB
    """
    cells = GatherCells(title="JS Job Wheel").get_cells_data()
    google_sheet = MemberJobs(cells)
    JobWheelUpdate().insert(google_sheet.get_full_dict())
    global current_raw_data
    current_raw_data = JobWheelUpdate().retrieve()
    return redirect("/")


@app.route("/_get_dictionary")
def get_dictionary():
    """
    send json from flask to the js client.
    JS
    :return:
    """
    return jsonify(result=current_raw_data)


if __name__ == "__main__":
    app.run(debug=True)
