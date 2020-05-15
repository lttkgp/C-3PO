# Data Transfer Object- Responsible for carrying data between processes
from flask import current_app
from flask_restx import Namespace, fields


class FeedDto:
    ns = Namespace('feed', description='Feed Related operations')
    songObject = ns.model('songObject', {
        'caption': fields.String,
        'link': fields.String
    })

