from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

from create_schedule import CreateSchedule
from gather_cells import GatherCellsFromGoogle
from member_jobs import MemberJobs


class ConnectMongoDB:
    def __init__(self):
        uri = os.environ['uri']
        self.client = MongoClient(uri, server_api=ServerApi('1'))  # atlas
        # self.client = MongoClient()  # local, just for testing
        self.db = self.client["SCA_Job_Wheel"]
        self.collection = self.db["Jobs_points"]

    def insert(self, info: dict):
        self.collection.insert_one(info)

    def retrieve(self):
        last_entry = self.collection.find().limit(1).sort([('$natural', -1)])
        result = [i for i in last_entry][0]
        del result['_id']  # delete "_id" since 'Object of type ObjectId is not JSON serializable'
        return result


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