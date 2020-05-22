"""Register all namespaces and import API's from  controllers."""
from flask import Blueprint
from flask_restx import Api

from api.controller.feed_controller import feed_ns
from api.controller.test_controller import api as test_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Flask-RESTPlus common backend for LTT-KGP',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(test_ns, path='/v1')
api.add_namespace(feed_ns, path='/v1/feed')
