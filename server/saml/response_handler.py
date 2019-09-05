import datetime
from typing import Mapping

from flask import session
from flask_saml2.sp import IdPHandler
from flask_saml2.sp.parser import ResponseParser
from flask_saml2.sp.xml_templates import AuthnRequest
from flask_saml2.utils import cached_property


def format_saml_datetime(dt):
    res = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return res


class MultipleAttributeValueResponseParser(ResponseParser):
    @cached_property
    def attributes(self) -> Mapping[str, str]:
        attributes = self._xpath(self.assertion, 'saml:AttributeStatement/saml:Attribute')
        res = {}
        for el in attributes:
            name = el.get("Name")
            values = self._xpath(el, 'saml:AttributeValue')
            res[name] = values[0].text if len(values) == 1 else [value.text for value in values]
        return res


class ResponseHandler(IdPHandler):

    def get_authn_request(self, template=AuthnRequest, **parameters):
        now = datetime.datetime.utcnow()
        new_parameters = {**parameters, **{"ISSUE_INSTANT": format_saml_datetime(now)}}
        return super().get_authn_request(template, **new_parameters)

    def make_login_request_url(self, relay_state):
        redirect_url = session["redirect_url"]
        return super().make_login_request_url(relay_state=redirect_url)

    def get_response_parser(self, saml_response):
        return MultipleAttributeValueResponseParser(self.decode_saml_string(saml_response),
                                                    certificate=self.certificate)
