import datetime
import json

from flask import Blueprint, request as current_request, session, url_for, redirect, current_app
from secrets import token_urlsafe
from sqlalchemy.orm import contains_eager
from werkzeug.exceptions import BadRequest

from server.api.base import json_endpoint, query_param, session_user_key, ok_response, ctx_logger
from server.db.db import User, RemoteAccount, Iuid, db, EmailVerification
from server.db.defaults import default_expiry_date
from server.db.models import flatten

user_api = Blueprint("user_api", __name__, url_prefix="/api/users")

redirect_url_session_key = "redirect_url"


def _merge_attributes(remote_attrs: dict, user_attrs: dict):
    def val(d: dict, key: str):
        v = d.get(key, [])
        return v if isinstance(v, list) else [v]

    return {key: list(set(val(remote_attrs, key) + val(user_attrs, key)))
            for key in set(remote_attrs) | set(user_attrs)}


@user_api.route("/check-identity", methods=["POST"], strict_slashes=False)
@json_endpoint
def user_search():
    iuid_values = current_request.get_json()["iuid"]
    users = User.find_by_iuid_values(iuid_values)
    if len(users) == 0:
        return None, 404
    if len(users) > 1:
        return None, 409
    user = users[0]
    iuids = [iuid.iuid for iuid in flatten([remote_account.iuids for remote_account in user.remote_accounts])]
    remote_account_attributes = {}
    for remote_account in user.remote_accounts:
        remote_account_attributes = _merge_attributes(remote_account_attributes, remote_account.attributes)
    res = {
        "result": "match",
        "matches": {},
        "user": {
            "cuid": user.cuid,
            "iuid": iuids,
        }
    }
    for k, v in _merge_attributes(remote_account_attributes, user.attributes).items():
        res["user"][k] = v
    for iuid in iuids:
        res["matches"][iuid] = iuid in iuid_values
    return res, 200


@user_api.route("/user-patch", methods=["PATCH"], strict_slashes=False)
@json_endpoint
def user_patch():
    data = current_request.get_json()
    user_cuid = data["cuid"]
    source_entity_id = data["source_entity_id"]
    iuid_values = data["iuid"]
    remote_account = RemoteAccount.query \
        .join(RemoteAccount.user) \
        .filter(User.cuid == user_cuid) \
        .filter(RemoteAccount.source_entity_id == source_entity_id) \
        .one()
    remote_account.iuids = [Iuid(iuid=iuid) for iuid in iuid_values]
    db.session.merge(remote_account)
    return ok_response, 201


@user_api.route("/me", strict_slashes=False)
@json_endpoint
def me():
    return load_user(), 200


def load_user():
    cuid = session[session_user_key]
    user = User.query \
        .join(User.remote_accounts) \
        .outerjoin(User.email_verifications) \
        .options(contains_eager(User.remote_accounts)) \
        .options(contains_eager(User.email_verifications)) \
        .filter(User.cuid == cuid) \
        .one()
    return user


@user_api.route("/", methods=["PUT"], strict_slashes=False)
@json_endpoint
def update():
    user = load_user()

    attributes = current_request.get_json()
    if "email" in attributes:
        user.email_verifications = [
            EmailVerification(code=token_urlsafe(6), email=email, expires_at=default_expiry_date) for email in
            attributes["email"]]

    db.session.merge(user)
    return user, 200


@user_api.route("/complete", methods=["PUT"], strict_slashes=False)
@json_endpoint
def complete():
    user = load_user()
    if len(user.email_verifications) > 0:
        raise BadRequest(description="Outstanding email verifications")

    user.is_complete = True
    db.session.merge(user)
    return {redirect_url_session_key: session[redirect_url_session_key]}, 200


@user_api.route("/login")
def login():
    session[redirect_url_session_key] = query_param(redirect_url_session_key, default=current_app.app_config.base_url)
    return redirect(url_for("flask_saml2_sp.login_idp", entity_id=current_app.app_config.saml.idp_entity_id))


@user_api.route("/verify", methods=["POST"], strict_slashes=False)
@json_endpoint
def verify_email():
    cuid = session[session_user_key]
    code = current_request.get_json()["code"]

    email_verification = EmailVerification.query \
        .join(EmailVerification.user) \
        .filter(User.cuid == cuid) \
        .filter(EmailVerification.code == code) \
        .filter(EmailVerification.expires_at >= datetime.datetime.now()) \
        .one()

    db.session.delete(email_verification)
    return ok_response, 201


@user_api.route("/error", methods=["POST"], strict_slashes=False)
@json_endpoint
def error():
    ctx_logger("user").exception(json.dumps(current_request.json))
    return {}, 201
