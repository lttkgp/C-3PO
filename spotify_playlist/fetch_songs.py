from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from c3po.db.models.user import UserPosts
from c3po.db.models.link import Link
from spotify_uri import get_spotify_id

engine = create_engine('postgresql+psycopg2://yash:root@localhost:5432/yash_test') 
engine.dialect.description_encoding = None
session = Session(bind=engine)

# get first 50 songs from the db
def get_song_names():
    songs = []
    for u , l in session.query(UserPosts,Link).filter(UserPosts.link_id==Link.id).all():
        if len(songs)<=50:
            if get_spotify_id(l.url) is not None:
                songs.append(get_spotify_id(l.url))
            else:
                continue
        else:
            break
    return songs




