from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from c3po.db.base import Base


class Link(Base):
    __tablename__ = "link"

    # Columns
    id = Column(Integer, primary_key=True)
    url = Column("url", String(160))
    platform = Column("platform", Integer)

    song_id = Column(Integer, ForeignKey("song.id"))

    post_count = Column("post_count", Integer)
    likes_count = Column("likes_count", Integer)
    views = Column("views", BigInteger)
    custom_popularity = Column("custom_popularity", Float)

    def __init__(self, url, platform, custom_popularity, views):
        self.url = url
        self.platform = platform
        self.custom_popularity = custom_popularity
        self.views = views

    def __str__(self):
        return self.url
