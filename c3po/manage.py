"""
Entrypoint of the application.

Manager is set up and the blueprint for the
application is created.
"""
import os
from logging import getLogger

from flask import Flask, current_app
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from c3po.logging_config import setup_logger
from c3po.app_config import config_by_name

setup_logger()
LOG = getLogger(__name__)
db = SQLAlchemy()


def initialize_extensions(app):
    db.init_app(app)
    LOG.info("database initialized successfully!")


def register_blueprints(app):
    from c3po.api import api_bp

    app.register_blueprint(api_bp)
    LOG.info("API blueprint registered!")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    LOG.info("app loaded with configuration {}!".format(config_name))

    with app.app_context():
        initialize_extensions(app)
        register_blueprints(app)
    return app


app = create_app(os.getenv("FLASK_ENV") or "dev")
migrate = Migrate(app, db)
