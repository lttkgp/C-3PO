from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
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

    def __init__(self, url, platform, song_id, post_count, likes_count):
        self.url = url
        self.platform = platform
        self.song_id = song_id
        self.post_count = post_count
        self.likes_count
