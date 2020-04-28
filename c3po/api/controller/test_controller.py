from flask import abort, request
from flask_restx import Resource, Namespace

api = Namespace('test', description='Hello World!')

@api.route('/')
class TestController(Resource):
    """ User Login Resource """
    @api.doc('Test controller to make sure project is set up!')
    def get(self):
        response_object = {
            'status' : 'Success!',
            'message' : '__init__()'
        }
        
        return response_object, 200