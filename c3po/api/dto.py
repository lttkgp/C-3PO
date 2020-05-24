# Data Transfer Object- Responsible for carrying data between processes
from flask import current_app
from flask_restx import Namespace

from marshmallow import Schema, fields

class PostDto(Schema):
    caption = fields.String()
    share_date = fields.DateTime()
    likes_count = fields.Integer()

class ArtistDto(Schema):
    name = fields.String()
    image = fields.String()

class SongDto(Schema):
    name = fields.String()
    image = fields.String()

class GenreDto(Schema):
    name = fields.String()

post_dto = PostDto()
artist_dto = ArtistDto()
song_dto = SongDto()
genre_dto = GenreDto()

class FeedDto:
    ns = Namespace('feed', description='Feed Related operations')
#     songObject = ns.model('songObject', {
#         'caption': fields.String,
#         'link': fields.String
#     })
