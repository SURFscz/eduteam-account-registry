import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler

import yaml
from flask import Flask, jsonify, request as current_request
from flask_mail import Mail
from flask_migrate import Migrate
from munch import munchify
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import flasgger

from server.api.aup import aup_api
from server.api.base import base_api
from server.api.dynamic_extended_json_encoder import DynamicExtendedJSONEncoder
from server.api.provision import provision_api
from server.api.user import user_api
from server.db.db import db, db_migrations
from server.saml.service_provider import configure_saml
from server.tools import read_file


def _init_logging(is_test):
    if is_test:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    else:
        formatter = logging.Formatter("EAR: %(asctime)s %(name)s %(levelname)s %(message)s")

        handler = TimedRotatingFileHandler(f"{os.path.dirname(os.path.realpath(__file__))}/../log/ear.log",
                                           when="midnight", backupCount=30)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        debug_handler = TimedRotatingFileHandler(f"{os.path.dirname(os.path.realpath(__file__))}/../log/ear_debug.log",
                                                 when="midnight", backupCount=30)
        debug_handler.setFormatter(formatter)
        debug_handler.setLevel(logging.DEBUG)

        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        logger.addHandler(handler)
        logger.addHandler(debug_handler)


config_file_location = os.environ.get("CONFIG", "config/config.yml")
config = munchify(yaml.load(read_file(config_file_location), Loader=yaml.FullLoader))
config.base_url = config.base_url[:-1] if config.base_url.endswith("/") else config.base_url

test = os.environ.get("TESTING")
profile = os.environ.get("PROFILE")

is_local = profile is not None and profile == "local"
is_test = test is not None and bool(int(test))

_init_logging(is_test or is_local)


def page_not_found(_):
    return jsonify({"message": f"{current_request.base_url} not found"}), 404


logger = logging.getLogger("main")
logger.info(f"Initialize server with profile {profile}")

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'eduTEAMS User Registry',
    'description': 'user registration application, which can be used to register federated user accounts',
    'version': '0.1',
    'openapi': '3.0.2',
    'uiversion': 3,
}
swagger = flasgger.Swagger(app)

app.secret_key = config.secret_key

app.register_blueprint(base_api)
app.register_blueprint(aup_api)
app.register_blueprint(user_api)
if test or is_local:
    app.register_blueprint(provision_api)

app.register_error_handler(404, page_not_found)

app.config["SQLALCHEMY_DATABASE_URI"] = config.database.uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = is_local or is_test

app.config["TESTING"] = test
app.config["MAIL_SERVER"] = config.mail.host
app.config["MAIL_PORT"] = int(config.mail.port)
app.config["OPEN_MAIL_IN_BROWSER"] = os.environ.get("OPEN_MAIL_IN_BROWSER", 0)
app.config["LOCAL"] = is_local

app.mail = Mail(app)

app.json_encoder = DynamicExtendedJSONEncoder

db.init_app(app)
app.db = db

app.app_config = config
app.app_config["profile"] = profile

configure_saml(app)

Migrate(app, db)
result = None
with app.app_context():
    while result is None:
        try:
            result = db.engine.execute(text("SELECT 1"))
        except OperationalError:
            logger.info("Waiting for the database...")
            time.sleep(1)

db_migrations(config.database.uri)

# WSGI production mode dictates that no flask app is actually running
if is_local:
    app.run(port=8080, debug=False, host="0.0.0.0", threaded=True)
