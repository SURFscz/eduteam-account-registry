import uuid

from flask import session
from flask_saml2.sp import AuthData
from munch import munchify

from server.api.base import session_user_key
from server.db.db import User
from server.saml.service_provider import sp
from server.test.abstract_test import AbstractTest


class TestServiceProvider(AbstractTest):

    def test_login_successful(self):
        iuid_values = [str(uuid.uuid4()), str(uuid.uuid4())]
        auth_data = AuthData(handler=munchify({"entity_id": "http://mocksp"}),
                             nameid="name_id",
                             nameid_format="nameid_format",
                             attributes={
                                 "urn:oid:0.9.2342.19200300.100.1.3": "jdoe@example.com",
                                 "urn:oid:2.16.840.1.113730.3.1.241": "John Doe",
                                 "urn:oid:1.3.6.1.4.1.5923.1.1.1.7": ["teachers", "members"],
                                 "urn:oid:1.3.6.1.4.1.34998.3.3.1.5": iuid_values,
                                 "urn:oid:1.3.6.1.4.1.5923.1.1.1.1": iuid_values,
                                 "urn:oid:1.3.6.1.4.1.25178.1.2.9": "example.com"
                             },
                             session_id="session_id")
        response = sp.login_successful(auth_data, "relay_state")
        self.assertEqual("http://localhost:3000/registration", response.location)
        user = User.query.filter(User.cuid == session[session_user_key]).one()
        self.assertEqual(False, user.is_complete)
        self.assertEqual("jdoe@example.com", user.remote_accounts[0].attributes["mail"])
