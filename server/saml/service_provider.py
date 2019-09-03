import OpenSSL
from flask import url_for, redirect, current_app
import os
from flask_saml2.sp import ServiceProvider, AuthData


def read_file(file_name):
    file = f"{os.path.dirname(os.path.realpath(__file__))}/{file_name}"
    with open(file) as f:
        return f.read()


class SP(ServiceProvider):
    def get_default_login_return_url(self):
        return url_for("base_api.index", _external=True)

    def get_sp_entity_id(self) -> str:
        return "https://eduteam-account-registry-localhost"

    def login_successful(self, auth_data: AuthData, relay_state: str):
        self.set_auth_data_in_session(auth_data)
        return redirect(current_app.app_config.base_url)


sp = SP()


def configure_saml(app):
    app.config["SAML2_SP"] = {
        "issuer": "https://eduteam-account-registry-localhost",
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
