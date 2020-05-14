from flask import abort, request
from flask_restx import Resource, Namespace, reqparse
from flask_restx.inputs import datetime_from_iso8601
from ..service.feed_service import FeedService
from ..dto import FeedDto

api = FeedDto.api
songObject = FeedDto.songObject

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int)
parser.add_argument('genre', type=str)
parser.add_argument('from', type=datetime_from_iso8601)
parser.add_argument('to', type=datetime_from_iso8601)


@api.route('/popular')
class FeedPopular(Resource):
    """ User Login Resource """
    @api.doc('Popular songs (most liked)')
    @api.marshal_list_with(songObject)
    @api.expect(parser)
    def get(self): 
        args = parser.parse_args()
        resp = FeedService.get_from_to(args['from'], args['to'])
        
        if resp[1] != 200:
            abort(403, resp[0])
        else:
            return resp

@api.route('/latest')
class FeedLatest(Resource):
    @api.doc('Latest feed')
    def get(self):
        resp = FeedService.get_latest_posts()
        #TODO: Complete the helper function used above
        
        if resp[1] != 200:
            abort(403, resp[0])
        else:
            return resp