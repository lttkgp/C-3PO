from urllib.parse import quote_plus

from c3po.utils.config import read_config


def _get_mongo_uri():
    MONGO_CONFIG = read_config("database.ini", "mongo")
    if "user" in MONGO_CONFIG:
        mongo_uri = "mongodb+srv://{user}:{password}@{host}/{database}".format(
            user=MONGO_CONFIG["user"],
            password=quote_plus(MONGO_CONFIG["password"]),
            host=MONGO_CONFIG["host"],
            database=MONGO_CONFIG["database"],
        )
        return mongo_uri
    else:
        mongo_uri = "mongodb://{host}:{port}/{database}".format(
            host=MONGO_CONFIG["host"],
            port=MONGO_CONFIG["port"],
            database=MONGO_CONFIG["database"],
        )
        return mongo_uri


def _get_postgres_uri():
    POSTGRES_CONFIG = read_config("database.ini", "postgresql")
    postgres_uri = "postgresql://{user}:{password}@{host}/{database}".format(
        user=POSTGRES_CONFIG["user"],
        password=quote_plus(POSTGRES_CONFIG["password"]),
        host=POSTGRES_CONFIG["host"],
        database=POSTGRES_CONFIG["database"],
    )
    return postgres_uri


MONGO_URI = _get_mongo_uri()
POSTGRES_URI = _get_postgres_uri()
