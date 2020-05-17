import json

from pymongo import MongoClient

from c3po.db.common.db_config import MONGO_URI

MC = MongoClient(MONGO_URI).get_database()


def post(data):
    print(json.dumps(data, indent=4, sort_keys=True))
    posts = MC["posts"]
    db_post = posts.find_one_and_replace(
        filter={"id": data["id"]}, replacement=data, upsert=True
    )
    return db_post
