from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from c3po.db.models.song import Song

engine = create_engine('Database URL') 
engine.dialect.description_encoding = None
session = Session(bind=engine)

# get first 50 songs from the db
def get_songs():
    songs = []
    q = session.query(Song).limit(50).all()
    for i in q:
        songs.append(i.name)
    return songs