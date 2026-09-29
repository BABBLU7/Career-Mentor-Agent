"""Load database/pathways.json into MongoDB.

Usage:
    pip install pymongo
    python database/seed_mongodb.py

Optional environment variables:
    MONGO_URI  (default: mongodb://127.0.0.1:27017)
    MONGO_DB   (default: career_mentor)
"""
import json
import os
from pathlib import Path

from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://127.0.0.1:27017")
MONGO_DB = os.environ.get("MONGO_DB", "career_mentor")
DATA_FILE = Path(__file__).parent / "pathways.json"


def main():
    with open(DATA_FILE, encoding="utf-8") as f:
        pathways = json.load(f)

    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    collection = client[MONGO_DB]["pathways"]

    collection.delete_many({})
    collection.insert_many(pathways)
    collection.create_index("id", unique=True)

    print(f"Inserted {collection.count_documents({})} pathways into "
          f"{MONGO_DB}.pathways at {MONGO_URI}")


if __name__ == "__main__":
    main()
