"""
Core script. Structure to be changed later.
"""
import argparse

from c3po.job.utils import facebook as facebookutils
from c3po.job.utils import lttkgp_archive
from c3po.utils import config

constants = config.read_config("config.ini", "facebook")


def add_post_to_db(post):
    old_post = lttkgp_archive.post(post)
    return old_post


def update_posts_db(next_link=""):
    duplicate_count = 0
    feed_chunk = facebookutils.get_feed(next_link)
    for post in feed_chunk["data"]:
        old_post = add_post_to_db(post)
        if old_post:
            duplicate_count = duplicate_count + 1
    while "paging" in feed_chunk:
        next_link = feed_chunk["paging"]["next"]
        if constants.get("FEED_FIRST_TIME") or duplicate_count < constants.get(
            "FEED_CHECK_DEPTH"
        ):
            feed_chunk = facebookutils.get_feed(next_link)
            for post in feed_chunk["data"]:
                old_post = add_post_to_db(post)
                if old_post:
                    duplicate_count = duplicate_count + 1
        else:
            break
