import re
from datetime import datetime, timedelta
from logging import getLogger

from c3po.api.dto import artist_dto, post_dto, song_dto
from c3po.api.service.paginate import get_paginated_response
from c3po.db.base import session_factory, session_scope
from c3po.db.models.artist import ArtistGenre, ArtistSong
from c3po.db.models.link import Link
from c3po.db.models.user import UserPosts

LOG = getLogger(__name__)


def get_yt_id(url):
    pattern = re.compile(
        r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})"
    )
    match = pattern.match(url)
    if not match:
        return None
    return match.group("id")


def format(session, post):
    link = post.link
    song = link.song
    id = get_yt_id(post.link.url)
    artists = [
        artist_song.artist
        for artist_song in session.query(ArtistSong)
        .filter(ArtistSong.song == song)
        .all()
    ]
    genres = []
    for artist in artists:
        artist_genres = [
            artist_genre.genre
            for artist_genre in session.query(ArtistGenre)
            .filter(ArtistGenre.artist == artist)
            .all()
        ]
        genres += artist_genres

    return {
        "link": link.url,
        "id": id,
        "post_count": link.post_count,
        "postdata": post_dto.dump(post),
        "metadata": {
            "song": song_dto.dump(link.song),
            "artists": [artist_dto.dump(artist) for artist in artists],
            "genre": [genre.name for genre in genres],
        },
    }


class FeedService:
    @staticmethod
    def get_posts_in_interval(
        from_=datetime.now() - timedelta(days=3), to_=datetime.now()
    ):
        try:
            session = session_factory()
            posts = (
                session.query(UserPosts)
                .filter(UserPosts.share_date >= from_)
                .filter(UserPosts.share_date <= to_)
                .all()
            )

            return posts, 200

        except BaseException:
            LOG.error(
                f"Failed to fetch data with params from_ = {from_}, to_ = {to_}. Try later.",
                exc_info=True,
            )
            response_object = {
                "status": "fail",
                "message": "Try again",
            }
            return response_object, 500

    @staticmethod
    def get_latest_posts(url, start, limit):
        with session_scope() as session:
            try:
                total = session.query(UserPosts).count()
                posts = (
                    session.query(UserPosts)
                    .filter(UserPosts.share_date <= datetime.now())
                    .order_by(UserPosts.share_date.desc())
                    .offset(start)
                    .limit(limit)
                    .all()
                )
                paginated_response = get_paginated_response(
                    posts, url, total, start, limit
                )
                paginated_response["posts"] = [
                    format(session, post) for post in paginated_response["posts"]
                ]

                return paginated_response, 200

            except BaseException:
                LOG.error(
                    f"Failed to fetch data with param start = {start}, limit = {limit}. Try later.",
                    exc_info=True,
                )
                response_object = {
                    "status": "fail",
                    "message": "Try again",
                }
                return response_object, 500

    @staticmethod
    def get_popular_posts(url, n, start, limit):
        """ Retrieves the most popular posts in the past n days"""
        with session_scope() as session:
            try:
                all_posts = (
                    session.query(UserPosts)
                    .filter(UserPosts.share_date <= datetime.now() + timedelta(days=1))
                    .filter(UserPosts.share_date >= datetime.now() - timedelta(days=n))
                    .order_by(UserPosts.likes_count.desc())
                )
                total = all_posts.count()
                posts = all_posts.offset(start).limit(limit).all()

                paginated_response = get_paginated_response(
                    posts, url, start=start, limit=limit, total=total
                )
                paginated_response["posts"] = [
                    format(session, post) for post in paginated_response["posts"]
                ]

                return paginated_response, 200

            except BaseException:
                LOG.error(
                    f"Failed to fetch data with param n = {n}, start = {start}, limit = {limit} . Try later.",
                    exc_info=True,
                )
                response_object = {
                    "status": "fail",
                    "message": "Try again",
                }
                return response_object, 500

    @staticmethod
    def get_frequent_posts(url, start, limit):
        with session_scope() as session:
            try:
                total = session.query(UserPosts).count()
                posts = (
                    session.query(UserPosts)
                    .filter(UserPosts.share_date <= datetime.now())
                    .join(UserPosts.link)
                    .order_by(Link.post_count.desc())
                    .offset(start)
                    .limit(limit)
                    .all()
                )

                paginated_response = get_paginated_response(
                    posts, url, total, start=start, limit=limit
                )
                paginated_response["posts"] = [
                    format(session, post) for post in paginated_response["posts"]
                ]

                return paginated_response, 200

            except BaseException:
                LOG.error(
                    f"Failed to fetch data with param limit_ = {limit}. Try later.",
                    exc_info=True,
                )
                response_object = {
                    "status": "fail",
                    "message": "Try again",
                }
                return response_object, 500
