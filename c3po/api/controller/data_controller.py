import os

from flask import abort, request
from flask_restx import Namespace, Resource, reqparse

from c3po.api.dto import DataDto
from c3po.api.service.data_service import DataService

data_ns = DataDto.ns

parser = reqparse.RequestParser()


@data_ns.route("/post")
@data_ns.header("whoami")
class UpdatePost(Resource):
    """ Update Post Resource """

    @data_ns.doc("Update a post")
    def post(self):
        if os.getenv("WHOAMI") != request.headers.get("whoami"):
            abort(403, {"success": False})
        response, status = DataService.UpdateOrCreate(request.data)
        if status != 200:
            abort(403, response)
        else:
            return response, status
