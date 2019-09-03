import datetime

from flask_saml2.sp import IdPHandler
from flask_saml2.sp.xml_templates import AuthnRequest
from flask_saml2.utils import get_random_id


def format_saml_datetime(dt):
    res = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return res


class ResponseHandler(IdPHandler):

    def get_authn_request(self, template=AuthnRequest, **parameters):
        now = datetime.datetime.utcnow()
        new_parameters = {**parameters, **{"ISSUE_INSTANT": format_saml_datetime(now)}}
        return super().get_authn_request(template, **new_parameters)

    def make_login_request_url(self, relay_state):
        return super().make_login_request_url(relay_state=get_random_id())
