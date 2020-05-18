from pymongo import MongoClient
from c3po.db.common.db_config import MONGO_URI
from c3po.job.utils.metadata import insert_metadata
from isodate import parse_datetime

MC = MongoClient(MONGO_URI).get_database()


def first_time_init():
    posts = MC["posts"]
    for data in posts.find():
        try:
            data['link']
            print(data)
            insert_metadata(data)
            # TODO: Remove break after testing
        except:
            pass


if __name__ == "__main__":
    first_time_init()
