# -*- coding: future_fstrings -*-
import datetime
import uuid

from secrets import token_urlsafe

from server.db.db import User, RemoteAccount, Iuid, EmailVerification, Aup, metadata
from server.db.defaults import default_expiry_date

john_email = "john.doe@example.org"

email_code = token_urlsafe(6)

john_cuid = str(uuid.uuid4())
john_iuids = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]

source_entity_id = "http://mock-idp"

def _persist(db, *objs):
    for obj in objs:
        db.session.add(obj)


def seed(db):
    tables = reversed(metadata.sorted_tables)
    for table in tables:
        db.session.execute(table.delete())
    db.session.commit()

    remote_account_attributes = {
        "name": [
            "Jane Doe",
            "髙橋大輔"
        ],
        "email": "jane.doe@example.org",
        "affiliation": ["employee", "member@example.org"]
    }


    remote_accounts = [RemoteAccount(source_entity_id=source_entity_id, source_display_name="John  Doe",
                                     attributes=remote_account_attributes,
                                     iuids=[Iuid(iuid=iuid) for iuid in john_iuids])]
    aups = [Aup(au_version="1.0", agreed_at=datetime.datetime.now())]
    email_verifications = [EmailVerification(code=email_code, email=john_email, expires_at=default_expiry_date())]

    john_attributes = {**remote_account_attributes, **{
        "postal_address": "Gebäude 465\nRaum 325\nBrandenburgische Straße 85\nBerlin",
        "country": "Germany",
        "email": "jdoe@google.com",
        "preferred_language": "zh-hant"
    }}
    john = User(cuid=john_cuid, attributes=john_attributes, is_complete=True, is_deleted=False, is_disabled=False,
                remote_accounts=remote_accounts, aups=aups, email_verifications=email_verifications)

    _persist(db, john)

    db.session.commit()
