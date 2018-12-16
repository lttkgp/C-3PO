"""
Core script. Structure to be changed later.
"""
import argparse

from utils import facebook as facebookutils
from utils import consolidate, lttkgp_archive
import constants


def consolidate_metadata(metadata):
    artists = consolidate.artists(metadata)
    song = consolidate.song(metadata)
    genres = consolidate.genres(metadata)
    consolidated_metadata = {
        'artists': artists,
        'song': song,
        'genres': genres,
    }
    return consolidated_metadata


def update_posts_db():
    duplicate_count = 0
    next_link = ""
    feed_chunk = facebookutils.get_feed(next_link)
    for post in feed_chunk['data']:
        old_post = lttkgp_archive.post(post)
        if old_post:
            duplicate_count = duplicate_count + 1
    while 'paging' in feed_chunk:
        next_link = feed_chunk['paging']['next']
        if constants.FEED_FIRST_TIME or duplicate_count < constants.FEED_CHECK_DEPTH:
            feed_chunk = facebookutils.get_feed(next_link)
            for post in feed_chunk['data']:
                old_post = lttkgp_archive.post(post)
                if old_post:
                    duplicate_count = duplicate_count + 1
        else:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        help="What would you like c3po to do today?",
        type=str,
        choices=["update_posts_db"])
    args = parser.parse_args()
    if args.command == 'update_posts_db':
        update_posts_db()
