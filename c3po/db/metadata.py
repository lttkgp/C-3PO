import logging
import time
from datetime import datetime

from httplib2 import ServerNotFoundError
from isodate import ISO8601Error, parse_datetime
from music_metadata_extractor import SongData

from c3po.db.base import session_scope
from c3po.db.models import (Artist, ArtistGenre, ArtistSong, Genre, Link, Song,
                            SongGenre, User, UserLikes, UserPosts)

logger = logging.getLogger(__name__)


def insert_metadata(raw_data):
    url = raw_data.get("link")
    if url:
        with session_scope() as session:
            try:
                data = SongData(url)
                # This is a placeholder for until we can fetch real user details
                user = _insert_default_user(session)
                new_link = _insert_post(url, user, data.extraAttrs, raw_data, session)
                if new_link:
                    if data.track and data.artists:
                        new_song = _insert_song(data.track, session)
                        new_link.song_id = new_song.id
                        for artist_data in data.artists:
                            new_artist = _insert_artist(artist_data, session)
                            _insert_artist_song(new_artist, new_song, session)
                            _insert_song_genre(artist_data, new_song, session)
                    else:
                        new_song = _insert_song(data.extraAttrs, session)
                        new_link.song_id = new_song.id
            except ServerNotFoundError:
                print("Google API unreachable!")
                time.sleep(30)
            except Exception as e:
                if str(e) == "Unsupported URL!" or str(e) == "Video unavailable!":
                    pass
                else:
                    data = SongData(url)
                    user = _insert_default_user(session)
                    new_link = _insert_post(
                        url, user, data.extraAttrs, raw_data, session
                    )


def _insert_post(url, user, extras, raw_data, session):
    try:
        date_time = parse_datetime(raw_data["created_time"])
    except ISO8601Error:
        date_time = datetime.now()
    if not raw_data.get("message") or len(raw_data.get("message")) > 160:
        caption = ""
    else:
        caption = raw_data.get("message").strip()
    facebook_id = raw_data["id"]
    likes_count = raw_data["reactions"]["summary"]["total_count"]
    permalink_url = raw_data["permalink_url"]
    existing_post = session.query(UserPosts).filter(UserPosts.facebook_id == facebook_id).first()
    if not existing_post:
        new_link = _insert_link(url, extras, session)
        if not new_link:
            new_link = session.query(Link).filter(Link.url == url).first()
            new_post = UserPosts(
                user, new_link, date_time, caption, facebook_id, permalink_url
            )
            new_post.likes_count = likes_count
            session.add(new_post)
            logger.info(f"New post added. facebook_id: {facebook_id}")
            return None
        new_post = UserPosts(user, new_link, date_time, caption, facebook_id, permalink_url)
        new_post.likes_count = likes_count
        session.add(new_post)
        logger.info(f"New post added. facebook_id: {facebook_id}")
        return new_link
    else:
        logger.info(f"Existing post with facebook_id {facebook_id} found")
        if(likes_count != existing_post.likes_count):
            existing_post.likes_count = likes_count
            return None


def _insert_artist_song(new_artist, new_song, session):
    new_artist_song = ArtistSong(new_artist, new_song)
    session.add(new_artist_song)


def _insert_link(url, extras, session):
    query = session.query(Link).filter(Link.url == url).first()
    if not query:
        views = int(extras["youtube"]["views"])
        custom_popularity = get_custom_popularity(extras)
        temp_link = Link(url, 0, custom_popularity, views)
        temp_link.post_count = 1
        session.add(temp_link)
        logger.info(f"New link added. URL: {url}")
        return temp_link
    else:
        query.post_count += 1
        logger.info(f"Existing link found. URL: {url}")
        return None


def _insert_song(track_data, session):
    if isinstance(track_data, dict):
        new_song = Song(
            track_data["youtube"]["title"],
            track_data["youtube"]["posted_date"],
            None,
            None,
            None,
            None,
            None,
        )

        session.add(new_song)
        session.flush()
        return new_song
    try:
        date = datetime.strptime(track_data.year, "%Y-%m-%d")
    except ValueError:
        date = datetime.strptime(track_data.year, "%Y")
    except BaseException:
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


def get_custom_popularity(extras):
    tz = extras["youtube"]["posted_date"].tzinfo
    delta = datetime.now(tz) - extras["youtube"]["posted_date"]
    days_since_posted = delta.days if delta.days > 0 else 1
    factor = 24 * 60 * 60
    score = float(int(extras["youtube"]["views"]) / (days_since_posted * factor))
    return score


def _insert_song_genre(artist_data, new_song, session):
    for temp_genre in artist_data.genres:
        new_genre = _insert_genre(temp_genre, session)
        query = (
            session.query(SongGenre)
            .filter(SongGenre.song_id == new_song.id)
            .filter(SongGenre.genre_id == new_genre.id)
            .first()
        )

        if not query:
            new_song_genre = SongGenre(new_genre, new_song)
            new_song_genre.genre_count = 1
            session.add(new_song_genre)
        else:
            query.genre_count += 1
