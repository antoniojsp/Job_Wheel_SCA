from pymongo import MongoClient
from pymongo.server_api import ServerApi

class JobWheelUpdate:
    def __init__(self):
        uri = "mongodb+srv://petiteurl:antonio12@cluster0.1ra6dk3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client["SCA_Job_Wheel"]
        self.collection = self.db["Jobs_points"]

    def insert(self, info: dict):
        self.collection.insert_one(info)

    def retrieve(self):
        return self.collection.find_one()

# a = Jobs("JS Job Wheel", "./credentials.json")
# b = JobWheelUpdate()
# b.insert(a.get_full_dict())
