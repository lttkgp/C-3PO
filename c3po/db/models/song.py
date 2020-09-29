from sqlalchemy import (Boolean, Column, Date, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import backref, relationship

from c3po.db.base import Base


class SongGenre(Base):
    __tablename__ = "song_genre"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)
    genre_count = Column(Integer, default=0)

    # Relationships
    genre = relationship(
        "Genre", backref=backref("genre_songs", cascade="all, delete-orphan")
    )
    song = relationship(
        "Song", backref=backref("song_genres", cascade="all, delete-orphan")
    )

    # Helper methods
    def __init__(self, genre=None, song=None):
        self.genre = genre
        self.song = song


class Song(Base):
    __tablename__ = "song"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column("name", String(320))
    release_date = Column("release_date", Date)
    explicit = Column("explicit", Boolean)
    popularity = Column("popularity", Float)
    image = Column("Image", String(160))
    # Self-referential relationship to model song covers
    cover = Column("cover", Boolean)
    original_id = Column(Integer, ForeignKey("song.id"))
    covers = relationship("Song")

    # Relationships
    links = relationship("Link", backref="song")

    def __init__(
        self, name, release_date, explicit, popularity, image, cover, original_id,
    ):
        self.name = name
        self.release_date = release_date
        self.explicit = explicit
        self.popularity = popularity
        self.image = image
        self.cover = cover
        self.original_id = original_id
