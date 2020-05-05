from c3po.db.dao import *
from c3po.db.common.base import session_scope
from datetime import datetime
from music_metadata_extractor import SongData

def insert(url, user, date_time=datetime.now()):
    with session_scope() as session:
        data = SongData(url)
        new_link = _insert_post(url, user, date_time, session)
        if(new_link):
            new_song = _insert_song(data.track, session)
            new_link.song_id = new_song.id
            for artist_data in data.artists:
                new_artist = _insert_artist(artist_data, session)
                _insert_artist_song(new_artist, new_song, session)


def _insert_post(url, user, date_time, session):
    new_link = _insert_link(url, session)
    if(not new_link):
        query = session.query(Link).filter(Link.url == url).first()
        new_post = Post(query, user, date_time)
        session.add(new_post)
        return None
    new_post = Post(new_link, user, date_time)
    session.add(new_post)
    return new_link

def _insert_artist_song(new_artist, new_song, session):
    new_artist_song = ArtistSong(new_artist, new_song)
    session.add(new_artist_song)

def _insert_link(url, session):
    query = session.query(Link).filter(Link.url == url).first()
    if(not query):
        temp_link = Link(url, 0)
        temp_link.post_count = 1
        session.add(temp_link)
        return temp_link
    else:
        query.post_count += 1
        return None

def _insert_song(track_data, session):
    try:
        date = datetime.strptime(track_data.year, "%Y-%m-%d")
    except ValueError:
        date = datetime.strptime(track_data.year, "%Y")
    except:
        date = None
    new_song = Song(
        track_data.name, 
        date,
        track_data.explicit, 
        track_data.popularity, 
        track_data.image_id, 
        track_data.is_cover,
        track_data.original_id
    )
    session.add(new_song)
    session.flush()
    return new_song

def _insert_artist(artist_data, session):
    query = session.query(Artist).filter(Artist.name == artist_data.name).first()
    if(not query):
        new_artist = Artist(artist_data.name, artist_data.image_id)
        session.add(new_artist)
        for temp_genre in artist_data.genres:
            new_genre = _insert_genre(temp_genre, session)
            new_artist_genre = ArtistGenre(new_artist, new_genre)
            session.add(new_artist_genre)
        return new_artist
    return query

def _insert_genre(genre_data, session):
    query = session.query(Genre).filter(Genre.name == genre_data).first()
    if(not query):
        temp_genre = Genre(genre_data)
        session.add(temp_genre)
        return temp_genre
    return query
