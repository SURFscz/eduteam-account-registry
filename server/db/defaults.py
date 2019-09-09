import datetime
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")


def default_expiry_date(json_dict=None):
    if json_dict is not None and "expires_at" in json_dict:
        ms = int(json_dict["expires_at"])
        return datetime.datetime.utcfromtimestamp(ms)
    return datetime.datetime.today() + datetime.timedelta(days=15)


def flatten(l):
    return [item for sublist in l for item in sublist]
