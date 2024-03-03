from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os


class ConnectMongoDB:
    def __init__(self):
        uri = os.environ['uri']
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["SCA_Job_Wheel"]
        self.collection = self.db["Jobs_points"]

    def insert(self, info: dict):
        self.collection.insert_one(info)

    def retrieve(self):
        last_entry = self.collection.find().limit(1).sort([('$natural', -1)])
        result = [i for i in last_entry][0]
        del result['_id']  # delete "_id" since 'Object of type ObjectId is not JSON serializable'
        return result

# a = Jobs("JS Job Wheel", "./credentials.json")
# b = JobWheelUpdate()
# pprint(JobWheelUpdate().retrieve())
# b.insert(a.get_full_dict())
