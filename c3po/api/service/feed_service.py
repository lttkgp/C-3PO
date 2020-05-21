from db.dao.user import UserPosts
from db.dao.artist import ArtistSong
from db.common.base import session_factory

from logging import getLogger
from datetime import datetime, timedelta

LOG = getLogger(__name__)

class FeedService:

    @staticmethod
    def get_posts_in_interval(from_=datetime.now() - timedelta(days=3), to_=datetime.now()):
        try:
            session = session_factory()
            posts = session.query(UserPosts).filter(UserPosts.share_date >= from_).filter(UserPosts.share_date <= to_).all()

            return posts, 200
                
        except BaseException:
            LOG.error(f'Failed to fetch data with params from_ = {from_}, to_ = {to_}. Try later.', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500
    
    @staticmethod
    def get_latest_posts(limit_):
        try:
            session = session_factory()
            posts = session.query(UserPosts).filter(UserPosts.share_date <= datetime.now()).limit(limit_).all()

            return posts, 200
                
        except BaseException:
            LOG.error(f'Failed to fetch data with param limit_ = {limit_}. Try later.', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500
    
