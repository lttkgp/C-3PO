from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from c3po.db.common.base import Base
from datetime import datetime

class Link(Base):
    __tablename__ = "link"

    # Columns
    id = Column(Integer, primary_key=True)
    url = Column("url", String(160))
    platform = Column("platform", Integer)

    song_id = Column(Integer, ForeignKey("song.id"))

    post_count = Column("post_count", Integer)
    likes_count = Column("likes_count", Integer)

    def __init__(self, url, platform):
        self.url = url
        self.platform = platform

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link_id = Column(Integer, ForeignKey("link.id"), primary_key=True)
    date_time = Column("datetime", DateTime)

    link = relationship(
        "Link", backref=backref("link", cascade="all, delete-orphan")
    )

    def __init__(self, link, date_time=datetime.now()):
        self.link = link
        self.date_time = date_time