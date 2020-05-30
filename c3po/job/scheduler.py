from apscheduler.schedulers.background import BackgroundScheduler

from c3po.job.utils.lttkgp_db import first_time_init

sched = BackgroundScheduler(daemon=True)


def update_db():
    first_time_init()


# sched.add_job(update_db)
sched.start()
