from server.db.db import User
from server.test.abstract_test import AbstractTest
from server.test.seed import john_iuids, john_cuid, source_entity_id
from urllib.parse import quote


class TestUser(AbstractTest):

    def test_check_identity(self):
        res = self.post("/api/users/check-identity", {"iuid": john_iuids[0:2]}, response_status_code=200)

        self.assertEqual(3, len(res["matches"]))
        self.assertEqual(2, len(dict(filter(lambda elem: elem[1], res["matches"].items()))))
        self.assertEqual("match", res["result"])
        self.assertEqual(john_cuid, res["user"]["cuid"])
        self.assertListEqual(["jane.doe@example.org", "jdoe@google.com"], sorted(res["user"]["email"]))
        self.assertListEqual(["Jane Doe", "髙橋大輔"], sorted(res["user"]["name"]))

    def test_user_patch(self):
        self.patch("/api/users", {"source_entity_id": source_entity_id, "cuid": john_cuid, "iuid": ["1", "2"]})
        user = User.query.filter(User.cuid == john_cuid).one()
        iuids = user.remote_accounts[0].iuids

        self.assertListEqual(["1", "2"], [iuid.iuid for iuid in iuids])
