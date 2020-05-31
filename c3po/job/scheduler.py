import argparse
import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from c3po.job.methods import repopulate_mongo, repopulate_postgres, update_mongo

sched = BackgroundScheduler(daemon=True)


@sched.scheduled_job(
    "interval",
    id="periodic_update_mongo",
    next_run_time=datetime.datetime.now(),
    minutes=15,
)
def periodic_update_mongo():
    update_mongo()


def instant_update_mongo():
    sched.get_job(job_id="periodic_update_mongo").modify(
        next_run_time=datetime.datetime.now()
    )


def instant_repopulate_mongo():
    repopulate_mongo()


def instant_repopulate_postgres():
    repopulate_postgres()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trigger C3PO jobs")
    parser.add_argument(
        "job_type",
        help="Which job would you like to run?",
        type=str,
        choices=[
            "instant_update_mongo",
            "instant_repopulate_mongo",
            "instant_repopulate_postgres",
        ],
    )
    args = parser.parse_args()
    if args.job_type == "instant_update_mongo":
        instant_update_mongo()
    elif args.job_type == "instant_repopulate_mongo":
        instant_repopulate_mongo()
    elif args.job_type == "instant_repopulate_postgres":
        instant_repopulate_postgres()
    else:
        print("Invalid job type!")
    sched.start()
