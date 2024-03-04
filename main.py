from create_schedule import CreateSchedule
from flask import Flask, render_template, redirect, jsonify
from gather_cells import GatherCellsFromGoogle
from member_jobs import MemberJobs
from update import ConnectMongoDB

app = Flask(__name__)

current_information_from_mongo = ConnectMongoDB().retrieve()


@app.route("/")
def index():
    return render_template('index.html',
                           title=current_information_from_mongo['Current term name'])


@app.route("/update")
def update_job_wheel():
    """
    google_sheet gets all the data from Google Sheets and transform it into a dictionary
    to be stored by JobWheelUpdate().insert() in MongoDB
    """
    cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()
    google_sheet_dictionary = MemberJobs(cells)  # convert the cells in a dictionary with all the information

    ConnectMongoDB().insert(google_sheet_dictionary.get_full_dict())
    global current_information_from_mongo
    current_information_from_mongo = ConnectMongoDB().retrieve()  # updates the global variable, same information for all users
    return redirect("/")  # return to the index


@app.route("/_get_dictionary")
def get_dictionary():
    """
    send json from flask (retrieve from MongoDB) to the js client.
    JS
    :return:
    """
    return jsonify(result=current_information_from_mongo)


if __name__ == "__main__":
    app.run(debug=True)
