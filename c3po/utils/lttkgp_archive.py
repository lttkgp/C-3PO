import json

from pymongo import MongoClient

from config import config

DB_CONFIG = config('database.ini', 'mongo')
MONGODB_URI = "mongodb://{host}:{port}/{database}".format(
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    database=DB_CONFIG['database'])
MC = MongoClient(MONGODB_URI).get_database()


def post(data):
    print(json.dumps(data, indent=4, sort_keys=True))
    posts = MC['posts']
    db_post = posts.find_one_and_replace(
        filter={'id': data['id']}, replacement=data, upsert=True)
    return db_post
