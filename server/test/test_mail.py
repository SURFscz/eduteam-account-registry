from server.mail import mail_verify_mail
from server.test.abstract_test import AbstractTest


class TestMail(AbstractTest):

    def test_send_verification_mail(self):
        mail = self.app.mail
        with mail.record_messages() as outbox:
            ctx = {"salutation": "Dear John,", "code": "123456", "email": "jdoe@example.org"}
            mail_verify_mail(ctx, ["test@example.com"])
            self.assertEqual(1, len(outbox))
            mail_msg = outbox[0]
            self.assertListEqual(["test@example.com"], mail_msg.recipients)
            self.assertEqual("eduTEAMS <no-reply@eduteams.org>", mail_msg.sender)
            self.assertTrue("123456" in mail_msg.html)

