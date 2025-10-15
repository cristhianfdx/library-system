import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


def get_mongo_collection(name: str) -> Collection:
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    db: Database = client["bookmanager"]
    return db[name]
