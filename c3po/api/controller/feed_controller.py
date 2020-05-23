from datetime import datetime, timedelta

from flask import abort, request
from flask_restx import Namespace, Resource, reqparse
from flask_restx.inputs import datetime_from_iso8601

from api.dto import FeedDto
from api.service.feed_service import FeedService

feed_ns = FeedDto.ns
songObject = FeedDto.songObject

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, default=10)
parser.add_argument('genre', type=str)
parser.add_argument('from', type=datetime_from_iso8601, help="Inclusive")
parser.add_argument('to', type=datetime_from_iso8601, help="Exclusive")


@feed_ns.route('/interval')
class FeedPopular(Resource):
    """ User Login Resource """
    @feed_ns.doc('Popular songs (most liked)')
    @feed_ns.marshal_list_with(songObject)
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        if(args['from'] and args['to']):
            response, status = FeedService.get_posts_in_interval(
                args['from'], args['to'])
        else:
            response, status = FeedService.get_posts_in_interval()

        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route('/latest')
class FeedLatest(Resource):
    @feed_ns.doc('Latest feed')
    @feed_ns.marshal_list_with(songObject)
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_latest_posts(args['limit'])
        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route('/popular')
class FeedLatest(Resource):
    popular_parser = parser
    popular_parser.add_argument('past', type=int, help='Days in the past')

    @feed_ns.doc('Latest popular songs')
    @feed_ns.marshal_list_with(songObject)
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_popular_posts(
            args['to'], args['past'])
        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route('/frequent')
class FeedFrequent(Resource):
    @feed_ns.doc('Most frequent songs')
    @feed_ns.marshal_list_with(songObject)
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_frequent_posts(args['limit'])
        if status != 200:
            abort(403, response)
        else:
            return response, status
