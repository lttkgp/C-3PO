from pymongo import MongoClient
from c3po.db.common.base import session_factory
from c3po.db.dao import user, link
from c3po.db.common.db_config import MONGO_URI

MC = MongoClient(MONGO_URI).get_database()


def post(data):
    # Create new session
    session = session_factory()

    lttkgp_user = user.User(
        "Default user",
        "1637563079601213",
        "https://user-images.githubusercontent.com/10023615/77320178-19fe9e00-6d36-11ea-9c0c-45f652a6da78.png",
    )
    song_link = link.Link(data["link"], 0)
    session.add(lttkgp_user)
    session.commit()


def first_time_init():
    posts = MC["posts"]
    latest = posts.find_one()
    print(latest)
    post(latest)


if __name__ == "__main__":
    first_time_init()
