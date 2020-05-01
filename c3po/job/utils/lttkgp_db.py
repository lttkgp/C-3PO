from pymongo import MongoClient
from c3po.db.common.db_config import MONGO_URI
from c3po.job.utils.metadata import insert
from datetime import datetime
from isodate import parse_datetime

MC = MongoClient(MONGO_URI).get_database()


def post(data):
    insert(data['link'], parse_datetime(data['created_time']))


def first_time_init():
    posts = MC["posts"]
    latest = posts.find_one()
    print(latest)
    post(latest)


if __name__ == "__main__":
    first_time_init()
