"""Register all namespaces and import API's from  controllers."""
from flask import Blueprint
from flask_restx import Api

from c3po.api.controller.feed_controller import feed_ns

api_bp = Blueprint("api", __name__)

api = Api(
    api_bp,
    title="Flask-RESTPlus common backend for LTT-KGP",
    version="1.0",
    description="a boilerplate for flask restplus web service",
)

api.add_namespace(feed_ns, path="/v1/feed")
