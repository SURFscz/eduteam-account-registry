from flask import Blueprint, request as current_request, session, url_for, redirect

from server.api.base import json_endpoint
from server.db.db import User, RemoteAccount, Iuid, db
from server.db.models import flatten

user_api = Blueprint("user_api", __name__, url_prefix="/api/users")


def _store_user_in_session(user: User):
    session["user"] = {
        "id": user.id
    }


def _merge_attributes(remote_attrs: dict, user_attrs: dict):
    def val(d: dict, key: str):
        v = d.get(key, [])
        return v if isinstance(v, list) else [v]

    return {key: list(set(val(remote_attrs, key) + val(user_attrs, key))) \
            for key in set(remote_attrs) | set(user_attrs)}


@user_api.route("/check-identity", methods=["POST"], strict_slashes=False)
@json_endpoint
def user_search():
    iuid_values = current_request.get_json()["iuid"]
    users = User.query.join(User.remote_accounts).join(RemoteAccount.iuids).filter(
        Iuid.iuid.in_(iuid_values)).all()
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


@user_api.route("/", methods=["PATCH"], strict_slashes=False)
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
    return None, 201


@user_api.route("login", )
def login():
    login_url = url_for('flask_saml2_sp.login')
    return redirect(login_url)
