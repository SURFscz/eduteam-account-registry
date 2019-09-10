from sqlalchemy import or_

from server.db.db import User, EmailVerification
from server.test.abstract_test import AbstractTest
from server.test.seed import john_iuids, john_cuid, source_entity_id, email_code, email_code_expired, john_email_second, \
    john_email


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
        self.patch("/api/users/user-patch",
                   {"source_entity_id": source_entity_id, "cuid": john_cuid, "iuid": ["1", "2"]})
        user = User.query.filter(User.cuid == john_cuid).one()
        iuids = user.remote_accounts[0].iuids

        self.assertListEqual(["1", "2"], [iuid.iuid for iuid in iuids])

    def test_me(self):
        self.provision()
        res = self.get("/api/users/me")
        self.assertEqual(True, res["is_complete"])
        self.assertEqual("jdoe@google.com", res["attributes"]["email"])
        self.assertEqual("jane.doe@example.org", res["remote_accounts"][0]["attributes"]["email"])

    def test_login(self):
        res = self.get("/api/users/login", query_data={"redirect_url": "http://mock-sp"}, response_status_code=302)
        self.assertTrue(res.location.startswith("http://localhost/saml/login/"))

    def test_login_default_redirect_uri(self):
        self.get("/api/users/login", response_status_code=302)

    def test_verify_email_code(self):
        self.provision()
        self.post("/api/users/verify", body={"code": email_code, "email": john_email})
        self.assertEqual(EmailVerification.query.filter(EmailVerification.code == email_code).count(), 0)

    def test_verify_email_code_expired(self):
        self.provision()
        self.post("/api/users/verify", body={"code": email_code_expired, "email": john_email_second},
                  response_status_code=400)

    def test_update_user_attributes_required_emails(self):
        self.provision()
        res = self.put("/api/users", body={"names": ["John Doe"]}, response_status_code=400)
        self.assertEqual("Required key emails not in user attributes", res["message"])

    def test_update_user_attributes_sanity(self):
        self.provision()
        res = self.put("/api/users", body={"names": ["John Doe"], "emails": ["john.doe@example.org"], "bogus": "nope"})
        self.assertEqual(False, "bogus" in res["attributes"])

        self.assertListEqual(res["attributes"]["emails"], ["john.doe@example.org"])

    def test_update_user_attributes_bad_email(self):
        self.provision()
        res = self.put("/api/users", body={"names": ["John Doe"], "emails": ["nope"]}, response_status_code=400)
        self.assertEqual("Invalid email nope", res["message"])

    def test_complete(self):
        self.get("/api/users/login", query_data={"redirect_url": "http://mock-sp"}, response_status_code=302)
        self.provision()
        EmailVerification.query \
            .filter(or_(EmailVerification.code == email_code_expired, EmailVerification.code == email_code)) \
            .delete()

        self.put("api/users/complete", response_status_code=201)

        res = self.get("/api/users/me")
        self.assertEqual(True, res["is_complete"])

    def test_complete_outstanding_verifications(self):
        self.get("/api/users/login", query_data={"redirect_url": "http://mock-sp"}, response_status_code=302)
        self.provision()
        res = self.put("api/users/complete", response_status_code=400)
        self.assertEqual("Outstanding email verifications", res["message"])

    def test_verifications(self):
        self.provision()
        res = self.get("/api/users/verifications")
        self.assertListEqual(
            [{"email": "john.doe@example.org", "verified": False}, {"email": "jdoe@example.org", "verified": False}],
            res)
