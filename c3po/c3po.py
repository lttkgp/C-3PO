"""
Core script. Structure to be changed later.
"""
import argparse

from utils import facebook as facebookutils
from utils import consolidate, lttkgp_archive


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
    next_link = ""
    feed, next_link = facebookutils.get_feed(next_link)
    for post in feed:
        mongo_success = lttkgp_archive.post(post)
    return feed


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
