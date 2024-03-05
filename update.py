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
        :return:
        '''
        cells = GatherCellsFromGoogle(title="JS Job Wheel").get_cells_data()  # raw data
        # forming dictionary
        members_job_dictionary = MemberJobs(
            cells).get_full_dict()  # convert the cells in a dictionary with all the information
        schedule_matrix = CreateSchedule(cells).get_schedule_matrix()
        product = {
            "members_job": members_job_dictionary,
            "schedule_matrix": schedule_matrix
        }
        self.collection.insert_one(product)

    def retrieve(self):
        """
        Pull the last record in mongodb to be use by the client js to display all the information
        :return:
        """
        last_entry = self.collection.find().limit(1).sort([('$natural', -1)])
        result = [i for i in last_entry]
        number_documents = len(result)
        if number_documents == 0:  # if 0, database has no records and needs to be restored.
            raise ValueError("The database is empty and needs to be restored.")
        last_document = result[0]
        del last_document['_id']  # delete "_id" since 'Object of type ObjectId is not JSON serializable'
        return last_document

# cells = GatherCellsFromGoogle("JS Job Wheel").get_cells_data()
# members_job_dictionary = MemberJobs(cells).get_full_dict()  # convert the cells in a dictionary with all the information
# schedule_dictionary = CreateSchedule(cells).get_schedule()
# product = {
#     "members_job": members_job_dictionary,
#     "schedule": schedule_dictionary
# }
#
# mongo_conn = ConnectMongoDB()
# mongo_conn.insert(product)
# print(mongo_conn.retrieve())
