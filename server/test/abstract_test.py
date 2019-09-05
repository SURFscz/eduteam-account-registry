import json
import os
from base64 import b64encode

import requests
from flask_testing import TestCase

from server.api.base import trusted_api
from server.test.seed import seed, john_cuid

# See api_users in config/test_config.yml
BASIC_AUTH_HEADER = {"Authorization": f"Basic {b64encode(b'satosa:secret').decode('ascii')}"}


# The database is cleared and seeded before every test
class AbstractTest(TestCase):

    def setUp(self):
        db = self.app.db
        with self.app.app_context():
            seed(db)

    def create_app(self):
        return AbstractTest.app

    @classmethod
    def setUpClass(cls):
        os.environ["CONFIG"] = "config/test_config.yml"
        os.environ["TESTING"] = "1"

        from server.__main__ import app

        config = app.app_config
        config["profile"] = None
        config.test = True
        AbstractTest.app = app

    def provision(self, cuid=john_cuid):
        with requests.Session():
            self.client.post("/api/provision", data=json.dumps({"cuid": cuid}),
                             content_type="application/json")

    @staticmethod
    def trusted_api_call(url):
        return [True for u in trusted_api if u in url]

    def get(self, url, query_data={}, response_status_code=200):
        with requests.Session():
            response = self.client.get(url, headers=BASIC_AUTH_HEADER if self.trusted_api_call(url) else {},
                                       query_string=query_data)
            self.assertEqual(response_status_code, response.status_code, msg=str(response.json))
            return response.json if hasattr(response, "json") and response.json else response

    def post(self, url, body={}, response_status_code=201):
        return self._do_call(body, self.client.post, response_status_code, url)

    def patch(self, url, body={}, response_status_code=201):
        return self._do_call(body, self.client.patch, response_status_code, url)

    def put(self, url, body={}, response_status_code=201):
        return self._do_call(body, self.client.put, response_status_code, url)

    def _do_call(self, body, call, response_status_code, url):
        with requests.Session():
            response = call(url, headers=BASIC_AUTH_HEADER if self.trusted_api_call(url) else {}, data=json.dumps(body),
                            content_type="application/json")
            self.assertEqual(response_status_code, response.status_code, msg=str(response.json))
            return response.json
