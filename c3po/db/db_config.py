from urllib.parse import quote_plus

from c3po.utils.config import read_config


def _get_postgres_uri():
    POSTGRES_CONFIG = read_config("config.ini", "postgresql")
    postgres_uri = "postgresql://{user}:{password}@{host}/{database}".format(
        user=POSTGRES_CONFIG["user"],
        password=quote_plus(POSTGRES_CONFIG["password"]),
        host=POSTGRES_CONFIG["host"],
        database=POSTGRES_CONFIG["database"],
    )
    return postgres_uri


POSTGRES_URI = _get_postgres_uri()
