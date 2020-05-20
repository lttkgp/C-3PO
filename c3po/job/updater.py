"""
Core script. Structure to be changed later.
"""
import argparse

import c3po.constants as constants
from c3po.job.utils import facebook as facebookutils
from c3po.job.utils import lttkgp_archive


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
        if constants.FEED_FIRST_TIME or duplicate_count < constants.FEED_CHECK_DEPTH:
            feed_chunk = facebookutils.get_feed(next_link)
            for post in feed_chunk["data"]:
                old_post = add_post_to_db(post)
                if old_post:
                    duplicate_count = duplicate_count + 1
        else:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the job to fetch data from Graph API"
    )
    parser.add_argument(
        "command",
        help="What would you like c3po to do today?",
        type=str,
        choices=["update_posts_db"],
    )
    parser.add_argument("--nl", dest="next_link", type=str, default="")
    args = parser.parse_args()
    if args.command == "update_posts_db":
        update_posts_db(args.next_link)
