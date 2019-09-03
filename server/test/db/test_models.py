import datetime

import requests

from server.db.models import parse_date_fields
from server.test.abstract_test import AbstractTest, BASIC_AUTH_HEADER


class TestModels(AbstractTest):

    def test_validation_error(self):
        self.post("/api/services", response_status_code=400)

    def test_no_json(self):
        with requests.Session():
            res = self.client.post("/api/services", headers=BASIC_AUTH_HEADER)
            self.assertEqual(415, res.status_code)

            res = self.client.put("/api/services", headers=BASIC_AUTH_HEADER)
            self.assertEqual(415, res.status_code)

    def test_parse_date_fields(self):
        json_dict = {"updated_at": 1549367857 * 1000}
        parse_date_fields(json_dict)
        self.assertTrue(isinstance(json_dict["updated_at"], datetime.datetime))

    def test_update_not_found(self):
        self.put("/api/services", body={"id": -1, "entity_id": "some", "name": "some"}, response_status_code=404)
