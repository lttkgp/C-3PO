from flask import abort, request
from flask_restx import Namespace, Resource, reqparse

from c3po.api.dto import HealthDto

health_ns = HealthDto.ns


@health_ns.route("/")
class HealthCheck(Resource):
    """ Check API health """

    @health_ns.doc("Check API health")
    def get(self):
        return {"success": True}, 200
