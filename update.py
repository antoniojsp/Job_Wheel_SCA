from pprint import pprint

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

from create_schedule import CreateSchedule
from gather_cells import GatherCellsFromGoogle
from member_jobs import MemberJobs


class ConnectMongoDB:
    def __init__(self):
        uri = os.environ['uri']
        # self.client = MongoClient(uri, server_api=ServerApi('1'))  # atlas
        self.client = MongoClient()  # local, just for testing
        self.db = self.client["SCA_Job_Wheel"]
        self.collection = self.db["Jobs_points"]

    def update_database(self):
        '''
        Gather information from google sheets, form a dictionary and send it to mongodb
        It can restore the database back in a working state
        :return:
        '''
        cells: list[list[str]] = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()  # raw data
        schedule = CreateSchedule(cells)
        # forming dictionary
        members_job_dictionary: dict = MemberJobs(cells).get_full_dict()  # format cell info into a dictionary
        schedule_matrix: list[tuple] = schedule.get_schedule_matrix()
        schedule_per_day:dict = schedule.get_schedule_dict_per_day()

        product: dict = {
            "members_job": members_job_dictionary,
            "schedule_matrix": schedule_matrix,
            "schedule_per_day": schedule_per_day
        }
        self.collection.insert_one(product)

    def retrieve(self) -> dict:
        """
        Pull the last record in mongodb to be use by the client js to display all the information
        :return:
        """
        list_last_entry: list = self.collection.find().limit(1).sort([('$natural', -1)])
        result: list[dict] = [i for i in list_last_entry]
        number_documents = len(result)
        if number_documents == 0:  # if 0, database has no records and needs to be restored.
            raise ValueError("The database is empty and needs to be restored.")
        last_document = result[0]
        del last_document['_id']  # delete "_id" since 'Object of type ObjectId is not JSON serializable'
        return last_document


if __name__ == "__main__":
    mongo_conn = ConnectMongoDB()
    mongo_conn.update_database()
    pprint(mongo_conn.retrieve())
