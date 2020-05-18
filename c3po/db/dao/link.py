from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, BigInteger,Date
from sqlalchemy.orm import relationship, backref
from c3po.db.common.base import Base

class Link(Base):
    __tablename__ = "link"

    # Columns
    id = Column(Integer, primary_key=True)
    url = Column("url", String(160))
    platform = Column("platform", Integer)

    song_id = Column(Integer, ForeignKey("song.id"))

    post_count = Column("post_count", Integer)
    likes_count = Column("likes_count", Integer)

    yt_views = Column("yt_views", BigInteger)
    yt_date = Column("yt_date", Date)

    def __init__(self, url, platform):
        self.url = url
        self.platform = platform