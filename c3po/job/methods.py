import json

import pymongo
from pymongo import MongoClient

from c3po.db.db_config import MONGO_URI
from c3po.job import facebook as facebookutils
from c3po.job.metadata import insert_metadata
from c3po.utils import config

constants = config.read_config("config.ini", "facebook")
MC = MongoClient(MONGO_URI).get_database()


def _add_to_mongo_db(post):
    print(json.dumps(post, indent=4, sort_keys=True))
    all_posts = MC["posts"]
    old_post = all_posts.find_one_and_replace(
        filter={"id": post["id"]}, replacement=post, upsert=True
    )
    return old_post


def _parse_feed(next_link, check_duplicates):
    duplicate_count = 0
    feed_chunk = facebookutils.get_feed(next_link)
    for post in feed_chunk["data"]:
        old_post = _add_to_mongo_db(post)
        if old_post:
            duplicate_count = duplicate_count + 1
    while "paging" in feed_chunk:
        next_link = feed_chunk["paging"]["next"]
        if check_duplicates and duplicate_count >= int(
            constants.get("FEED_CHECK_DEPTH")
        ):
            break
        feed_chunk = facebookutils.get_feed(next_link)
        for post in feed_chunk["data"]:
            old_post = _add_to_mongo_db(post)
            if old_post:
                duplicate_count = duplicate_count + 1


def update_mongo(next_link=""):
    _parse_feed(next_link, True)


def repopulate_mongo(next_link=""):
    _parse_feed(next_link, False)


def repopulate_postgres():
    posts = MC["posts"]
    for data in posts.find().sort('created_time', pymongo.DESCENDING):
        try:
            print(data)
            insert_metadata(data)
        except Exception as ex:
            print("Metadata fetch failed")
            pass
