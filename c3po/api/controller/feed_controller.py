from flask import abort, request
from flask_restx import Resource, Namespace, reqparse
from flask_restx.inputs import date_from_iso8601
from ..service.feed_service import get_all
api = Namespace('feed', description='LTTKGP Feed')

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int)
parser.add_argument('genre', type=str)
parser.add_argument('from', type=date_from_iso8601)
parser.add_argument('to', type=date_from_iso8601)

'''
limit - to limit the number of responses (although we’ll use a default value if this is not specified)
genre - this is self explanatory
page - for pagination. Implementation of pagination can get quite tricky though - we’ll discuss this further / find reading material
from - Time period start (default to 7 days back for all endpoints if not specified explicitly)
to - Time period end (default to current time/date if not specified explicitly)
'''



@api.route('/popular')
class FeedPopular(Resource):
    """ User Login Resource """
    @api.doc('Popular songs (most liked)')
    @api.expect(parser)
    def get(self):
        args = parser.parse_args()
        response_object = get_all()
        return response_object, 200

@api.route('/latest')
class FeedLatest(Resource):
    @api.doc('Latest feed')
    def get(self):
        response_object = {
            'status' : 'Success! latest, bitch!!',
            'message' : '__init__()'
        }
        
        return response_object, 200