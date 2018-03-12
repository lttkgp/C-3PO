from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///lttkgp.db', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)

song_artist = Table('song_artist', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.song_id'), nullable=False),
    Column('artist_id', Integer, ForeignKey('artists.artist_id'), nullable=False))

genre_song = Table('genre_song', Base.metadata,
    Column('genre_id', Integer, ForeignKey('genres.genre_id'), nullable=False),
    Column('song_id', Integer, ForeignKey('songs.song_id'), nullable=False))

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    # user_picture = Column(String)
    posts = relationship('Post')

class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key=True)
    link_id = Column(Integer, ForeignKey('links.link_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_time = Column(DateTime)

class Song(Base):
    __tablename__ = 'songs'

    song_id = Column(Integer, primary_key=True)
    artists = relationship('Artist', secondary=song_artist, backref='songs')
    genres = relationship('Genre', secondary=genre_song, backref='songs')
    song_title = Column(String)
    links = relationship('Link')

class Genre(Base):
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String)

class Artist(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)

class Link(Base):
    __tablename__ = 'links'

    link_id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id'), nullable=False)
    link_type = Column(String)
    link_value = Column(Integer)
    posts = relationship('Post')

Base.metadata.create_all(engine)