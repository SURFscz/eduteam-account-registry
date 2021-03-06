import logging

from flask import session, g as request_context


class CustomAdapter(logging.LoggerAdapter):

    def __init__(self, logger):
        user_cuid = session["user"]["cuid"] if "user" in session else request_context.api_user.name \
            if "api_user" in request_context else "ext_api"
        super().__init__(logger, {"user": user_cuid})

    def process(self, msg, kwargs):
        return f"user: {self.extra['user']}, {msg}", kwargs
