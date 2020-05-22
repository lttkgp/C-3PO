from flask import abort, request
from flask_restx import Namespace, Resource

api = Namespace('test', description='Hello LTT-KGP!')


@api.route('/')
class TestController(Resource):
    """ User Login Resource """
    @api.doc('Test controller to make sure project is set up!')
    def get(self):
        response_object = {
            'status': 'Success!',
            'message': '__init__()'
        }

        return response_object, 200
