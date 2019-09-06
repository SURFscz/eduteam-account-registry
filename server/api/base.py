import json
import logging
import os
from functools import wraps
from pathlib import Path

from flask import Blueprint, jsonify, current_app, request as current_request, session
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import HTTPException, Unauthorized, BadRequest

from server.api.context_logger import CustomAdapter
from server.db.db import db

base_api = Blueprint("base_api", __name__, url_prefix="/")

white_listing = ["health", "config", "info", "provision", "login", "static"]
trusted_api = ["user-patch", "check-identity"]
session_user_key = "session_user_key"

ok_response = {"status": "ok"}


def _get_user(app_config, auth):
    if not auth:
        return None
    users = list(
        filter(lambda user: user.name == auth.username and user.password == auth.password, app_config.api_users))
    return users[0] if len(users) > 0 else None


def auth_filter(app_config):
    url = current_request.base_url

    for u in white_listing:
        if u in url:
            return

    trusted_api_call = [True for u in trusted_api if u in url]
    if session_user_key in session and not trusted_api_call:
        return

    auth = current_request.authorization
    api_user = _get_user(app_config, auth)
    if not auth and not api_user:
        raise Unauthorized(description="Invalid username or password")


def query_param(key, required=True, default=None):
    value = current_request.args.get(key, default=default)
    if required and value is None:
        raise BadRequest(f"Query parameter {key} is required, but missing")
    return value


def ctx_logger(name=None):
    return CustomAdapter(logging.getLogger(name))


def _add_custom_header(response):
    response.headers.set("x-session-alive", "true")
    response.headers["server"] = ""


_audit_trail_methods = ["PUT", "PATCH", "POST", "DELETE"]


def _audit_trail():
    method = current_request.method
    if method in _audit_trail_methods:
        msg = json.dumps(current_request.json) if method != "DELETE" else ""
        ctx_logger("base").info(f"Path {current_request.path} {method} {msg}")


def json_endpoint(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            session.modified = True
            auth_filter(current_app.app_config)
            body, status = f(*args, **kwargs)
            response = jsonify(body)
            _audit_trail()
            _add_custom_header(response)
            db.session.commit()
            return response, status
        except Exception as e:
            response = jsonify(message=e.description if isinstance(e, HTTPException) else str(e),
                               error=True)
            ctx_logger("base").exception(response)
            if isinstance(e, NoResultFound):
                response.status_code = 404
            elif isinstance(e, HTTPException):
                response.status_code = e.code
            else:
                response.status_code = 500
            _add_custom_header(response)
            db.session.rollback()
            return response

    return wrapper


@base_api.route("/health", strict_slashes=False)
@json_endpoint
def health():
    return {"status": "UP"}, 200


@base_api.route("/config", strict_slashes=False)
@json_endpoint
def config():
    def clean_url(url):
        return url[:-1] if url.endswith("/") else url

    base_url = current_app.app_config.base_url
    login_url = current_app.app_config.login_url
    return {"login_url": clean_url(login_url),
            "base_url": clean_url(base_url)}, 200


@base_api.route("/info", strict_slashes=False)
@json_endpoint
def info():
    file = Path(f"{os.path.dirname(os.path.realpath(__file__))}/git.info")
    if file.is_file():
        with open(str(file)) as f:
            return {"git": f.read()}, 200
    return {"git": "nope"}, 200
