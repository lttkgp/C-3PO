from c3po.db.base import session_scope
from c3po.db.models.user import UserPosts
from c3po.db.models.link import Link
from spotify_uri import get_spotify_id

# get first 50 songs from the db
def get_song_url():
    with session_scope() as session:
        songs = []
        for u,l in session.query(UserPosts,Link).filter(UserPosts.link_id==Link.id).limit(50).all():
            if len(songs)<=50:
                if get_spotify_id(l.url) is not None:
                    songs.append(get_spotify_id(l.url))
                else:
                    continue
            else:
                break
        return songs