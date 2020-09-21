from datetime import datetime, timedelta

from flask import abort, request
from flask_restx import Namespace, Resource, reqparse
from flask_restx.inputs import datetime_from_iso8601

from c3po.api.dto import FeedDto
from c3po.api.service.feed_service import FeedService

feed_ns = FeedDto.ns

parser = reqparse.RequestParser()

parser.add_argument("genre", type=str)
parser.add_argument("start", type=int, default=0)
parser.add_argument("limit", type=int, default=25)


@feed_ns.route("/interval")
class FeedPopular(Resource):
    interval_parser = parser
    interval_parser.add_argument("from", type=datetime_from_iso8601, help="Inclusive")
    interval_parser.add_argument("to", type=datetime_from_iso8601, help="Exclusive")
    """ User Login Resource """

    @feed_ns.doc("Popular songs (most liked)")
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        if args["from"] and args["to"]:
            response, status = FeedService.get_posts_in_interval(
                request.url, args["start"], args["limit"], args["from"], args["to"]
            )
        else:
            response, status = FeedService.get_posts_in_interval(
                request.url, args["start"], args["limit"]
            )

        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route("/latest")
class FeedLatest(Resource):
    @feed_ns.doc("Latest feed")
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_latest_posts(
            request.url, args["start"], args["limit"]
        )
        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route("/popular")
class FeedLatest(Resource):
    popular_parser = parser
    popular_parser.add_argument("n", type=int, help="Days in the past", default=7)

    @feed_ns.doc("Latest popular songs")
    @feed_ns.expect(popular_parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_popular_posts(
            request.url, args["n"], args["start"], args["limit"]
        )
        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route("/frequent")
class FeedFrequent(Resource):
    @feed_ns.doc("Most frequent songs")
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_frequent_posts(
            request.url, args["start"], args["limit"]
        )
        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route("/underrated")
class FeedUnderrated(Resource):
    @feed_ns.doc("Underrated songs")
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_underrated_posts(
            request.url, args["start"], args["limit"]
        )
        if status != 200:
            abort(403, response)
        else:
            return response, status


@feed_ns.route("/random")
class FeedUnderrated(Resource):
    @feed_ns.doc("Randomly shuffled songs")
    @feed_ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        response, status = FeedService.get_random_posts(
            request.url, args["start"], args["limit"]
        )
        if status != 200:
            abort(403, response)
        else:
            return response, status
