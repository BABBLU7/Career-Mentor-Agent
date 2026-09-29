import os

from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017")
MONGO_DB = os.environ.get("MONGO_DB", "career_mentor")

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    return _client[MONGO_DB]


def fetch_pathways():
    """Read all pathway documents from MongoDB (without the internal _id)."""
    return list(get_db()["pathways"].find({}, {"_id": 0}))
