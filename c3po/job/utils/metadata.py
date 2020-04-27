from c3po.db.dao import user, link, song, artist, genre
from c3po.db.common.base import session_factory
from datetime import datetime
from music_metadata_extractor import SongData
from contextlib import contextmanager

@contextmanager
def session_scope():
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        raise
        session.rollback()
    finally:
        session.close()


def insert(url):
    with session_scope() as session:
        data = SongData(url)
        new_link = _insert_link(url, session)
        if(new_link):
            new_song = _insert_song(data.track, session)
            _add_song_id(new_song, new_link, session)
            for artist_data in data.artists:
                new_artist = _insert_artist(artist_data, session)
                _insert_artist_song(new_artist, new_song, session)

def _add_song_id(new_song, new_link, session):
    new_link.song_id = new_song.id
    session.commit()

def _insert_artist_song(new_artist, new_song, session):
    new_artist_song = artist.ArtistSong(new_artist, new_song)
    session.add(new_artist_song)
    session.commit()


def _insert_link(url, session):
    query = session.query(link.Link).filter(link.Link.url == url).first()
    if(not query):
        temp_link = link.Link(url, 0)
        temp_link.post_count = 1
        session.add(temp_link)
        session.commit()
        return temp_link
    else:
        query.post_count += 1
        session.commit()
        return None

def _insert_song(track_data, session):
    try:
        date = datetime.strptime(track_data.year, "%Y-%m-%d")
    except ValueError:
        date = datetime.strptime(track_data.year, "%Y")
    except:
        date = None
    new_song = song.Song(
        track_data.name, 
        date,
        track_data.explicit, 
        track_data.popularity, 
        track_data.image_id, 
        track_data.is_cover,
        track_data.original_id
    )
    session.add(new_song)
    session.commit()
    return new_song

def _insert_artist(artist_data, session):
    query = session.query(artist.Artist).filter(artist.Artist.name == artist_data.name).first()
    if(not query):
        new_artist = artist.Artist(artist_data.name, artist_data.image_id)
        session.add(new_artist)
        session.commit()
        for temp_genre in artist_data.genres:
            new_genre = _insert_genre(temp_genre, session)
            new_artist_genre = artist.ArtistGenre(new_artist, new_genre)
            session.add(new_artist_genre)
            session.commit()
        return new_artist
    return query

def _insert_genre(genre_data, session):
    query = session.query(genre.Genre).filter(genre.Genre.name == genre_data).first()
    if(not query):
        temp_genre = genre.Genre(genre_data)
        session.add(temp_genre)
        session.commit()
        return temp_genre
    return query
