from logging import getLogger

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from c3po.app_config import config_by_name

LOG = getLogger(__name__)

LOG.info('configured logger!')

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    LOG.info('app loaded with configuration {}!'.format(config_name))

    app.app_context().push()
    LOG.info('application context pushed')

    db.init_app(app)
    LOG.info('database initialized successfully!')

    return app
