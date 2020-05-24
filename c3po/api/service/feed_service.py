from datetime import datetime, timedelta
from logging import getLogger

from api.dto import artist_dto, post_dto, song_dto
from db.common.base import session_factory
from db.dao.artist import ArtistGenre, ArtistSong
from db.dao.link import Link
from db.dao.user import UserPosts

LOG = getLogger(__name__)


def format(post):
    session = session_factory()
    link = post.link
    song = link.song
    artists = [artist_song.artist for artist_song in session.query(ArtistSong)
               .filter(ArtistSong.song == song).all()]
    genres = []
    for artist in artists:
        artist_genres = [artist_genre.genre for artist_genre in session.query(ArtistGenre)
                         .filter(ArtistGenre.artist == artist).all()]
        genres += artist_genres

    return {
        'link': link.url,
        'postdata': post_dto.dump(post),
        'metadata': {
            'song': song_dto.dump(link.song),
            'artists': [artist_dto.dump(artist) for artist in artists],
            'genre': [genre.name for genre in genres]
        }
    }


class FeedService:

    @staticmethod
    def get_posts_in_interval(from_=datetime.now() - timedelta(days=3), to_=datetime.now()):
        try:
            session = session_factory()
            posts = session.query(UserPosts).filter(UserPosts.share_date >= from_) \
                .filter(UserPosts.share_date <= to_).all()

            response = [format(post) for post in posts]
            return response, 200

        except BaseException:
            LOG.error(
                f'Failed to fetch data with params from_ = {from_}, to_ = {to_}. Try later.', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def get_latest_posts(limit_):
        try:
            session = session_factory()
            posts = session.query(UserPosts).filter(
                UserPosts.share_date <= datetime.now()).limit(limit_).all()

            response = [format(post) for post in posts]
            return response, 200

        except BaseException:
            LOG.error(
                f'Failed to fetch data with param limit_ = {limit_}. Try later.', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def get_popular_posts(to_=datetime.now(), past=1):
        try:
            session = session_factory()
            posts = session.query(UserPosts)\
                .filter(UserPosts.share_date <= to_ + timedelta(days=1))\
                .filter(UserPosts.share_date >= to_ - timedelta(days=past))\
                .order_by(UserPosts.likes_count.desc()).all()

            response = [format(post) for post in posts]
            return response, 200

        except BaseException:
            LOG.error(
                f'Failed to fetch data with param to_ = {to_}, past = {past}. Try later.', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def get_frequent_posts(limit_=10):
        try:
            session = session_factory()
            posts = session.query(UserPosts)\
                .filter(UserPosts.share_date <= datetime.now()).limit(limit_).all()

            postURLFreq = {}
            for post in posts:
                if post in postURLFreq:
                    postURLFreq[post.link.url] += 1
                else:
                    postURLFreq[post.link.url] = 1

            postURLFreq = {k: v for k, v in sorted(
                postURLFreq.items(), key=lambda x: x[1], reverse=True)}

            freqPosts = []

            for url, countURL in postURLFreq.items():
                postsWithURL = [post for post in posts if post.link.url == url]
                freqPosts.extend(postsWithURL)

            response = [format(post) for post in freqPosts]
            return response, 200

        except BaseException:
            LOG.error(
                f'Failed to fetch data with param limit_ = {limit_}. Try later.', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500
