# Data Transfer Object- Responsible for carrying data between processes
from flask import current_app
from flask_restx import Namespace
from marshmallow import Schema, fields


class FeedDto:
    ns = Namespace("Feed", description="Feed Related operations")


class DataDto:
    ns = Namespace("Data", description="Data Related operations")


class PostDto(Schema):
    caption = fields.String()
    share_date = fields.DateTime()
    likes_count = fields.Integer()
    permalink_url = fields.String()


class ArtistDto(Schema):
    name = fields.String()
    image = fields.String()


class SongDto(Schema):
    name = fields.String()
    image = fields.String()


post_dto = PostDto()
artist_dto = ArtistDto()
song_dto = SongDto()
