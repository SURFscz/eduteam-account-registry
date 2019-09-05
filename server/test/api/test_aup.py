from server.db.db import Aup, User
from server.test.abstract_test import AbstractTest
from server.test.seed import john_cuid


class TestUser(AbstractTest):

    @staticmethod
    def _aup_count():
        return Aup.query \
            .join(Aup.user) \
            .filter(User.cuid == john_cuid) \
            .count()

    def test_links(self):
        self.provision()
        links = self.get("/api/aup", response_status_code=200)
        self.assertEqual(True, "pdf" in links)
        self.assertEqual(True, "html" in links)

    def test_agree(self):
        pre_count = self._aup_count()
        self.provision()
        self.post("/api/aup/")

        post_count = self._aup_count()

        self.assertEqual(pre_count, post_count - 1)
