from flask import Blueprint, request as current_request, session

from server.api.base import json_endpoint, session_user_key

provision_api = Blueprint("provision_api", __name__, url_prefix="/api/provision")


@provision_api.route("/", methods=["POST"], strict_slashes=False)
@json_endpoint
def provision():
    session[session_user_key] = current_request.get_json()["cuid"]
    return None, 201
