from base64 import b64encode, b64decode
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def verify(message, signature, public_key):
    key = RSA.import_key(public_key)
    digest = SHA256.new(message.encode('utf-8'))
    try:
        pkcs1_15.new(key).verify(digest, b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False
