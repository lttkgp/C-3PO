from c3po.db.dao import *
from c3po.db.common.base import session_scope
from datetime import datetime
from music_metadata_extractor import SongData

def insert(url):
    with session_scope() as session:
        data = SongData(url)
        new_link = _insert_link(data.extraAttrs, url, session)
        if(new_link):
            new_song = _insert_song(data.track, session)
            new_link.song_id = new_song.id
            for artist_data in data.artists:
                new_artist = _insert_artist(artist_data, session)
                _insert_artist_song(new_artist, new_song, session)


def _insert_artist_song(new_artist, new_song, session):
    new_artist_song = artist.ArtistSong(new_artist, new_song)
    session.add(new_artist_song)

def _insert_link(extras, url, session):
    query = session.query(link.Link).filter(link.Link.url == url).first()
    views = extras['youtube']['views']
    date = extras['youtube']['posted_date']
    if(not query):
        temp_link = link.Link(url, 0)
        temp_link.post_count = 1
        temp_link.yt_views = views
        temp_link.yt_date = date

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
    session.flush()
    return new_song

def _insert_artist(artist_data, session):
    query = session.query(artist.Artist).filter(artist.Artist.name == artist_data.name).first()
    if(not query):
        new_artist = artist.Artist(artist_data.name, artist_data.image_id)
        session.add(new_artist)
        for temp_genre in artist_data.genres:
            new_genre = _insert_genre(temp_genre, session)
            new_artist_genre = artist.ArtistGenre(new_artist, new_genre)
            session.add(new_artist_genre)
        return new_artist
    return query

def _insert_genre(genre_data, session):
    query = session.query(genre.Genre).filter(genre.Genre.name == genre_data).first()
    if(not query):
        temp_genre = genre.Genre(genre_data)
        session.add(temp_genre)
        return temp_genre
    return query
