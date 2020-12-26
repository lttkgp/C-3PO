from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from c3po.db.base import Base


class ArtistGenre(Base):
    __tablename__ = "artist_genre"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey("artist.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genre.id"), primary_key=True)

    # Relationships
    genre = relationship(
        "Genre", backref=backref("genre_artists", cascade="all, delete-orphan")
    )
    artist = relationship(
        "Artist", backref=backref("artist_genres", cascade="all, delete-orphan")
    )

    # Helper methods
    def __init__(self, artist=None, genre=None):
        self.artist = artist
        self.genre = genre


class ArtistSong(Base):
    __tablename__ = "artist_song"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey("artist.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("song.id"), primary_key=True)

    # Relationships
    artist = relationship(
        "Artist", backref=backref("artist_songs", cascade="all, delete-orphan")
    )
    song = relationship(
        "Song", backref=backref("song_artists", cascade="all, delete-orphan")
    )

    # Helper methods
    def __init__(self, artist=None, song=None):
        self.artist = artist
        self.song = song


class Artist(Base):
    __tablename__ = "artist"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column("name", String(160))
    image = Column("image", String(160))

    # Helper methods
    def __init__(self, name, image):
        self.name = name
        self.image = image
