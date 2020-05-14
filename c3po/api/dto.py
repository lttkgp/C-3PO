# Data Transfer Object- Responsible for carrying data between processes
from flask import current_app
from flask_restx import Namespace, fields


class FeedDto:
    api = Namespace('feed', description='Feed Related operations')
    songObject = api.model('songObject', {
        'caption': fields.String,
        'link': fields.String()
    })

