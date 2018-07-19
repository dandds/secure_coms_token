import hashlib
import hmac
import base64

def make_token(key, data):
    formatted = ':'.join(data).encode()
    hashed = hmac.new(key.encode(), formatted, hashlib.sha256)
    return base64.urlsafe_b64encode(hashed.digest()).decode()

def validate_token(token, key, data):
    comp = make_token(key, data)
    return hmac.compare_digest(token, comp)
