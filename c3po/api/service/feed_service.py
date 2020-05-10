from c3po.db.dao.user import UserPosts
from c3po.db.dao.artist import ArtistSong
from c3po.db.common.base import session_scope

def get_all():
    with session_scope() as session:
        posts = session.query(UserPosts).all()
        return [
            {
                'caption': obj.caption
            } for obj in posts
        ]