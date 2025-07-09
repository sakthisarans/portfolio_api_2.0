from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Mongo:
    def __init__(self):
        mongo_url = os.getenv("MONGO_URI")
        mongo_db = os.getenv("MONGO_DB")
        client = MongoClient(mongo_url)
        self.mongo_db = client[mongo_db]

    def save(self, data: dict, collection: str,upsert: str = "_id"):
        coll = self.mongo_db[collection]
        # Use '_id' for upsert if present, else insert new
        if upsert in data and data[upsert]:
            result = coll.update_one(
                {upsert: data[upsert]},
                {"$set": data},
                upsert=True
            )
        else:
            result = coll.insert_one(data)
        return result
    def find(self, query: dict, collection: str):
        coll = self.mongo_db[collection]
        return coll.find_one(query)