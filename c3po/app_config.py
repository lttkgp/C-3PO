"""Define App level configuration for Dev, Testing and Production."""
import os

from c3po.db.db_config import POSTGRES_URI

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base Config."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = POSTGRES_URI


class DevelopmentConfig(Config):
    """Development Config, don't use on prod."""

    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing Config, use when running unit tests."""

    DEBUG = True
    TESTING = True
    HOST = "127.0.0.1"
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = os.getenv("TESTING_DATABASE_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    """Production config, use when deploying on server."""

    DEBUG = False
    HOST = "0.0.0.0"
    PORT = "443"
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config_by_name = dict(
    development=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)
