"""
Entrypoint of the application.

Manager is set up and the blueprint for the
application is created.
"""
import os
from logging import getLogger

from flask import Flask, current_app
from flask_cors import CORS

from c3po.app_config import config_by_name
from c3po.job.scheduler import setup_scheduler
from c3po.logging_config import setup_logger

setup_logger()
LOG = getLogger(__name__)


def register_blueprints(app):
    from c3po.api import api_bp
    from c3po.job import job_bp

    app.register_blueprint(api_bp)
    LOG.info("API blueprint registered!")

    app.register_blueprint(job_bp)
    LOG.info("Job blueprint registered!")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    LOG.info("app loaded with configuration {}!".format(config_name))

    CORS(app)
    LOG.info("Flask CORS setup successfully")
    with app.app_context():
        register_blueprints(app)

    return app

app = create_app(os.getenv("FLASK_ENV") or "development")

@app.cli.command()
def schedule():
    """Start the scheduler"""
    sched = setup_scheduler(fetch_fb_posts=True, process_posts=True)
    LOG.info("Scheduler setup successfully")
    sched.start()
