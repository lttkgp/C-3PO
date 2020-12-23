from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

from c3po.db.base import Base


class Link(Base):
    __tablename__ = "link"

    # Columns
    id = Column(Integer, primary_key=True)
    url = Column("url", String(160))
    platform = Column("platform", Integer)
    original_url = Column("original_url", String)
    song_id = Column(Integer, ForeignKey("song.id"))

    post_count = Column("post_count", Integer)
    likes_count = Column("likes_count", Integer)
    views = Column("views", BigInteger)
    custom_popularity = Column("custom_popularity", Float)

    def __init__(self, url, platform, custom_popularity, views, original_url):
        self.url = url
        self.platform = platform
        self.custom_popularity = custom_popularity
        self.views = views
        self.original_url = original_url

    def __str__(self):
        return self.url
