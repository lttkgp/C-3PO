import json
from urllib.parse import quote_plus
from pymongo import MongoClient
from c3po.utils.config import config

DB_CONFIG = config("database.ini", "mongo")
print(DB_CONFIG)
if "user" in DB_CONFIG:
    MONGODB_URI = "mongodb+srv://{user}:{password}@{host}/{database}".format(
        user=DB_CONFIG["user"],
        password=quote_plus(DB_CONFIG["password"]),
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
    )
else:
    MONGODB_URI = "mongodb://{host}:{port}/{database}".format(
        host=DB_CONFIG["host"], port=DB_CONFIG["port"], database=DB_CONFIG["database"]
    )
MC = MongoClient(MONGODB_URI).get_database()


def post(data):
    print(json.dumps(data, indent=4, sort_keys=True))
    posts = MC["posts"]
    db_post = posts.find_one_and_replace(
        filter={"id": data["id"]}, replacement=data, upsert=True
    )
    return db_post
