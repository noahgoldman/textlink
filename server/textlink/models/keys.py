from flask import request
import hmac, base64, hashlib

from textlink.models import Key

def sign(key, msg):
    hash = hmac.new(bytes(key.secret), bytes(msg), hashlib.sha256).digest()
    return base64.b64encode(hash)

def create(session, user):
    key = Key(user)
    session.add(key)
    session.commit()
    return key

#def auth(key_id, signature, msg):

