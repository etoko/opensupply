import hashlib

def sha256_digest(passwd):
    return hashlib.sha256(passwd).hexdigest()
