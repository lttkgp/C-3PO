from flask import abort, request
from flask_restx import Resource, Namespace, reqparse
from flask_restx.inputs import datetime_from_iso8601
from api.service.feed_service import FeedService
from api.dto import FeedDto

feed_ns = FeedDto.ns
songObject = FeedDto.songObject

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int)
parser.add_argument('genre', type=str)
parser.add_argument('from', type=datetime_from_iso8601)
parser.add_argument('to', type=datetime_from_iso8601)


@feed_ns.route('/popular')
class FeedPopular(Resource):
    """ User Login Resource """
    @feed_ns.doc('Popular songs (most liked)')
    @feed_ns.marshal_list_with(songObject)
    @feed_ns.expect(parser)
    def get(self): 
        args = parser.parse_args()
        response, status = FeedService.get_posts_in_interval(args['from'], args['to'])
        
        if status != 200:
            abort(403, response)
        else:
            return response, status

@feed_ns.route('/latest')
class FeedLatest(Resource):
    @feed_ns.doc('Latest feed')
    def get(self):
        response, status = FeedService.get_latest_posts()
        #TODO: Complete the helper function used above
        
        if status != 200:
            abort(403, response)
        else:
            return response, status