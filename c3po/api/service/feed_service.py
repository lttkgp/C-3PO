from datetime import datetime, timedelta

from c3po.db.common.base import session_scope
from c3po.db.dao.artist import ArtistSong
from c3po.db.dao.user import UserPosts

DEFAULT_TIME_PERIOD = timedelta(days=7)


def get_from_to(from_=datetime.now(), to_=datetime.now() - DEFAULT_TIME_PERIOD):
    with session_scope() as session:
        posts = session.query(UserPosts).filter(UserPosts.share_date >= from_)
        posts = posts.filter(UserPosts.share_date <= to_).all()
        return [
            {
                'caption': obj.caption,
                'url': obj.link.url
            } for obj in posts
        ]
