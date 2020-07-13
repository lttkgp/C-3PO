from logging import getLogger

from apscheduler.schedulers.background import BackgroundScheduler

from c3po.job.updater import update_posts_db
from c3po.job.utils.lttkgp_db import first_time_init
from c3po.utils.config import read_config

LOG = getLogger(__name__)
sched = BackgroundScheduler(daemon=True)
PROCESS_POSTS_FREQUENCY = int(
    read_config(section="scheduler")["PROCESS_POSTS_FREQUENCY"]
)
FB_FETCH_FREQUENCY = int(read_config(section="scheduler")["FB_FETCH_FREQUENCY"])


def setup_scheduler(fetch_fb_posts=True, process_posts=True):
    if fetch_fb_posts:
        sched.add_job(update_posts_db, "interval", minutes=FB_FETCH_FREQUENCY)
        LOG.info(
            f"Add scheduler job to Fetch FB posts every {FB_FETCH_FREQUENCY} minutes"
        )

    if process_posts:
        sched.add_job(first_time_init, "interval", minutes=PROCESS_POSTS_FREQUENCY)
        LOG.info(
            f"Add scheduler job to process Mongo posts every {PROCESS_POSTS_FREQUENCY} minutes"
        )

    return sched
