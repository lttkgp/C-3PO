from c3po.db.common.base import session_scope
from c3po.db.dao import Artist, ArtistGenre, ArtistSong
from c3po.db.dao import Genre
from c3po.db.dao import Link
from c3po.db.dao import Song, SongGenre
from c3po.db.dao import User, UserLikes, UserPosts
from datetime import datetime
from isodate import parse_datetime, ISO8601Error
from music_metadata_extractor import SongData


def insert_metadata(data):
    url = data["link"]
    with session_scope() as session:
        data = SongData(url)
        # This is a placeholder for until we can fetch real user details
        user = _insert_default_user(session)
        new_link = _insert_post(url, user, data, session)
        if new_link:
            new_song = _insert_song(data.track, session)
            new_link.song_id = new_song.id
            for artist_data in data.artists:
                new_artist = _insert_artist(artist_data, session)
                _insert_artist_song(new_artist, new_song, session)


def _insert_post(url, user, data, session):
    try:
        date_time = parse_datetime(data["created_time"])
    except ISO8601Error:
        date_time = datetime.now()
    caption = "" if data["message"] is None else data["message"].strip()
    facebook_id = data["id"]
    likes_count = data["reactions"]["summary"]["total_count"]
    new_link = _insert_link(url, session)
    if not new_link:
        query = session.query(Link).filter(Link.url == url).first()
        new_post = UserPosts(user, query, date_time, caption, facebook_id)
        new_post.likes_count = likes_count
        session.add(new_post)
        return None
    new_post = UserPosts(user, query, date_time, caption, facebook_id)
    new_post.likes_count = likes_count
    session.add(new_post)
    return new_link


def _insert_artist_song(new_artist, new_song, session):
    new_artist_song = ArtistSong(new_artist, new_song)
    session.add(new_artist_song)


def _insert_link(url, session):
    query = session.query(Link).filter(Link.url == url).first()
    if not query:
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
        track_data.original_id,
    )
    session.add(new_song)
    session.flush()
    return new_song


def _insert_artist(artist_data, session):
    query = session.query(Artist).filter(Artist.name == artist_data.name).first()
    if not query:
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
    if not query:
        temp_genre = Genre(genre_data)
        session.add(temp_genre)
        return temp_genre
    return query


def _insert_user(name, facebook_id, image, session):
    query = session.query(User).filter(User.facebook_id == facebook_id).first()
    if not query:
        new_user = User(name, facebook_id, image)
        session.add(new_user)
        return new_user
    return query


def _insert_default_user(session):
    return _insert_user(
        "Default User",
        "1637563079601213",
        "https://user-images.githubusercontent.com/10023615/77320178-19fe9e00-6d36-11ea-9c0c-45f652a6da78.png",
        session,
    )
