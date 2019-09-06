import datetime

from flask import Blueprint, current_app, session

from server.api.base import json_endpoint, ok_response, session_user_key
from server.db.db import User, Aup, db

aup_api = Blueprint("aup_api", __name__, url_prefix="/api/aup")


@aup_api.route("/", methods=["GET"], strict_slashes=False)
@json_endpoint
def links():
    from server.__main__ import read_file
    return {
               "pdf_link": current_app.app_config.aup.pdf_link,
               "pdf": current_app.app_config.aup.pdf,
               "html": read_file(f"./static/{current_app.app_config.aup.html}")
           }, 200


@aup_api.route("/", methods=["POST"], strict_slashes=False)
@json_endpoint
def agreed_aup():
    cuid = session[session_user_key]
    user = User.query \
        .filter(User.cuid == cuid) \
        .one()
    aup = Aup(au_version=current_app.app_config.aup.pdf, user=user,
              agreed_at=datetime.datetime.now())
    db.session.merge(aup)
    return ok_response, 201
