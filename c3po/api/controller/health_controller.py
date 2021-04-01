from flask import abort, request
from flask_restx import Namespace, Resource, reqparse

from c3po.api.dto import HealthDto
from c3po.api.service.health_service import get_active_status

health_ns = HealthDto.ns


@health_ns.route("/")
class HealthCheck(Resource):
    """ Check API health """

    @health_ns.doc("Check API health")
    def get(self):
        return {"success": True}, 200


@health_ns.route("/status")
class StatusCheck(Resource):
    """ Check if posts are active or stale """
    def get(self):
        if get_active_status():
            return {"status": "Active"}, 200
        return {"status": "Stale"}, 200
