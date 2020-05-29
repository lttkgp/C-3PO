from contextlib import contextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from c3po.db.db_config import POSTGRES_URI

engine = create_engine(POSTGRES_URI)
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()


def session_factory():
    from c3po.db.dao import artist, genre, link, song, user

    Base.metadata.create_all(engine)
    return _SessionFactory()


@contextmanager
def session_scope():
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        raise
        session.rollback()
    finally:
        session.close()
