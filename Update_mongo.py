from pprint import pprint
from pymongo import MongoClient
from Job import Jobs

class JobWheelUpdate:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client["SCA_Job_Wheel"]
        self.collection = self.db["Jobs_points"]

    def insert(self, info: dict):
        self.collection.insert_one(info)

    def retrieve(self):
        return self.collection.find_one()

# a = Jobs("JS Job Wheel", "./credentials.json")
# b = JobWheelUpdate()
# b.insert(a.get_full_dict())
