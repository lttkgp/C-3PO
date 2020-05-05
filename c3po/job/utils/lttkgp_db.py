from pymongo import MongoClient
from c3po.db.common.db_config import MONGO_URI
from c3po.job.utils.metadata import insert
from datetime import datetime
from isodate import parse_datetime
from c3po.db.dao.user import User
from c3po.db.common.base import session_scope

MC = MongoClient(MONGO_URI).get_database()


def post(data, user):
    insert(data['link'], user, parse_datetime(data['created_time']))


def first_time_init():
    with session_scope() as session:
        lttkgp_user = _insert_user(
            "Default user",
            "1637563079601213",
            "https://user-images.githubusercontent.com/10023615/77320178-19fe9e00-6d36-11ea-9c0c-45f652a6da78.png",
            session
        )
    
    posts = MC["posts"]
    latest = posts.find_one()
    print(latest)
    post(latest, lttkgp_user)

def _insert_user(name, facebook_id, image, session):
    query = session.query(User).filter(User.facebook_id == facebook_id).first()
    if(not query):
        new_user = User(name, facebook_id, image)
        session.add(new_user)
        return new_user
    return query

if __name__ == "__main__":
    first_time_init()
