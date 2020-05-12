from flask import abort, request
from flask_restx import Resource, Namespace, reqparse
from flask_restx.inputs import datetime_from_iso8601
from ..service.feed_service import get_from_to
api = Namespace('feed', description='LTTKGP Feed')

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int)
parser.add_argument('genre', type=str)
parser.add_argument('from', type=datetime_from_iso8601)
parser.add_argument('to', type=datetime_from_iso8601)


@api.route('/popular')
class FeedPopular(Resource):
    """ User Login Resource """
    @api.doc('Popular songs (most liked)')
    @api.expect(parser)
    def get(self): 
        args = parser.parse_args()
        response_object = get_from_to(args['from'], args['to'])
        return response_object, 200

@api.route('/latest')
class FeedLatest(Resource):
    @api.doc('Latest feed')
    def get(self):
        return response_object, 200