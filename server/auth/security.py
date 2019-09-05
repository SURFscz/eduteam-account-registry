import hashlib


def secure_hash(secret):
    return hashlib.sha256(bytes(secret, "utf-8")).hexdigest()
