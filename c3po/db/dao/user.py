from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from db.common.base import Base


class UserLikes(Base):
    __tablename__ = "user_likes"

    # Columns
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    link_id = Column(Integer, ForeignKey("link.id"), primary_key=True)
    reaction_type = Column(Integer)

    # Relationships
    link = relationship(
        "Link", backref=backref("liked_by", cascade="all, delete-orphan")
    )
    user = relationship("User", backref=backref("likes", cascade="all, delete-orphan"))

    # Helper methods
    def __init__(self, link=None, user=None, reaction_type=None):
        self.link = link
        self.user = user
        self.reaction_type = reaction_type


class UserPosts(Base):
    __tablename__ = "user_posts"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    link_id = Column(Integer, ForeignKey("link.id"), primary_key=True)
    share_date = Column(DateTime)
    caption = Column(String(160))
    facebook_id = Column(String(160))
    likes_count = Column(Integer)

    # Relationships
    link = relationship(
        "Link", backref=backref("posted_by", cascade="all, delete-orphan")
    )
    user = relationship(
        "User", backref=backref("user_links", cascade="all, delete-orphan")
    )

    # Helper methods
    def __init__(self, user=None, link=None, share_date=None, caption=None, facebook_id=None):
        self.user = user
        self.link = link
        self.share_date = share_date
        self.caption = caption
        self.facebook_id = facebook_id


class User(Base):
    __tablename__ = "user"

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column("name", String(32), nullable=False)
    facebook_id = Column("facebook_id", String, unique=True)
    image = Column("image", String(160))
    post_count = Column("post_count", Integer)
    liked_count = Column("liked_count", Integer)
    likes_count = Column("likes_count", Integer)
    __table_args__ = (UniqueConstraint("id", "facebook_id", name="user_id"),)

    def __init__(self, name, facebook_id, image):
        self.name = name
        self.facebook_id = facebook_id
        self.image = image
