from pprint import pprint

from create_schedule import CreateSchedule
from flask import Flask, render_template, redirect, jsonify
from gather_cells import GatherCellsFromGoogle
from member_jobs import MemberJobs
from update import ConnectMongoDB

app = Flask(__name__)


try:
    current_information_from_mongo = ConnectMongoDB().retrieve()
except ValueError as err:
    current_information_from_mongo = ConnectMongoDB().update_database()


@app.route("/")
def index():
    return render_template('index.html',
                           title=current_information_from_mongo["members_job"]['Current term name'])


@app.route("/update")
def update_job_wheel():
    """
    google_sheet gets all the data from Google Sheets and transform it into a dictionary
    to be stored by JobWheelUpdate().insert() in MongoDB
    """
    global current_information_from_mongo
    current_information_from_mongo = ConnectMongoDB().update_database()
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
