from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from c3po.db.common.base import Base


class Genre(Base):
    __tablename__ = "genre"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column("name", String(32))

    # Relationships
    artists = association_proxy("genre_artists", "artist")

    # Helper methods
    def __init__(self, name):
        self.name = name
