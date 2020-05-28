from isodate import parse_datetime
from pymongo import MongoClient

from c3po.db.common.db_config import MONGO_URI
from c3po.job.utils.metadata import insert_metadata

MC = MongoClient(MONGO_URI).get_database()


def first_time_init():
    posts = MC["posts"]
    for data in posts.find():
        try:
            insert_metadata(data)
            print(data['id'])
        # TODO: Remove break after testing
        except Exception as e:
            pass


if __name__ == "__main__":
    first_time_init()
