import datetime


def default_expiry_date(json_dict=None):
    if json_dict is not None and "expires_at" in json_dict:
        ms = int(json_dict["expires_at"])
        return datetime.datetime.utcfromtimestamp(ms)
    return datetime.datetime.today() + datetime.timedelta(days=15)
