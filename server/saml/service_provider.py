import os
import uuid

import OpenSSL
from flask import redirect, current_app, session
from flask_saml2.sp import ServiceProvider, AuthData

from server.api.base import session_user_key
from server.db.db import User, db, RemoteAccount, Iuid
from server.saml.saml_mapping import saml2_oid_mapping, unidentified_idp


def read_file(file_name):
    file = f"{os.path.dirname(os.path.realpath(__file__))}/{file_name}"
    with open(file) as f:
        return f.read()


class SP(ServiceProvider):
    def get_default_login_return_url(self):
        return current_app.app_config.base_url

    def get_sp_entity_id(self) -> str:
        return current_app.app_config.saml.sp_entity_id

    def login_successful(self, auth_data: AuthData, relay_state: str):
        attributes = auth_data.to_dict()["data"]["attributes"]
        user_attributes = {saml2_oid_mapping[k]: v for k, v in attributes.items() if k in saml2_oid_mapping}
        iuid_values = user_attributes[current_app.app_config.saml.hash_identifiers_attribute]
        if not iuid_values:
            raise ValueError(f"No attribute value(s) for {current_app.app_config.saml.hash_identifiers_attribute}")
        if isinstance(iuid_values, str):
            iuid_values = [iuid_values]
        users = User.find_by_iuid_values(iuid_values)
        if len(users) == 0:
            source_entity_id = user_attributes.get("schacHomeOrganization", unidentified_idp)
            remote_accounts = [RemoteAccount(source_entity_id=source_entity_id,
                                             source_display_name=user_attributes["displayName"],
                                             attributes=user_attributes,
                                             iuids=[Iuid(iuid=iuid) for iuid in iuid_values])]
            cuid = str(uuid.uuid4())
            session[session_user_key] = cuid
            db.session.add(User(cuid=cuid, remote_accounts=remote_accounts))
            db.session.commit()
            return redirect(f"{current_app.app_config.base_url}/registration")
        if len(users) == 1:
            session[session_user_key] = users[0].cuid
            path = "account" if users[0].is_complete else "registration"
            return redirect(f"{current_app.app_config.base_url}/{path}")
        if len(users) > 1:
            return redirect(f"{current_app.app_config.base_url}/error?type=multiple_users_found")


sp = SP()


def configure_saml(app):
    app.config["SAML2_SP"] = {
        "issuer": app.app_config.saml.sp_entity_id,
        "certificate": OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, read_file("sp_cert.pem")),
        "private_key": OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, read_file("sp_key.pem")),
    }
    app.config["SAML2_IDENTITY_PROVIDERS"] = [
        {
            "CLASS": "server.saml.ResponseHandler",
            "OPTIONS": {
                "entity_id": app.app_config.saml.idp_entity_id,
                "sso_url": app.app_config.saml.idp_sso_url,
                "certificate": OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                                               read_file("engine.test.surfconext.nl.pem")),
            },
        }
    ]
    app.register_blueprint(sp.create_blueprint(), url_prefix='/saml/')
