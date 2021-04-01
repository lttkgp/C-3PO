from logging import getLogger
from c3po.db.models.user import UserPosts
from c3po.db.base import session_scope
from datetime import datetime, timedelta
from c3po.config.config import read_config

LOG = getLogger(__name__)
MAX_ACTIVE_DAYS = read_config(section="api")["MAX_ACTIVE_DAYS"]

def get_active_status():
    """ Checks the share_date of the latest post. """
    with session_scope() as session:
        posts = (
            session.query(UserPosts)
            .order_by(UserPosts.share_date.desc())
            .limit(1)
            .all()
        )
        latest_post = posts[0]
        print(type(MAX_ACTIVE_DAYS))
        if datetime.now() - latest_post.share_date <= timedelta(days=int(MAX_ACTIVE_DAYS)):
            return True
        return False
