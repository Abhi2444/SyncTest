import hashlib
import json
import time
import uuid
from datetime import datetime

import jsonschema

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

#------------------------------------------------------------------------------------
customer_client_identifier = "eyJhbGciOiJIUzUxMiJ9.eyJjbGllbnRJZGVudGlmaWVyIjoiNGZlMTY4ZjUtZDNhOC00MTRjLWJkNmQtZGNmMGU4ZDAwNzliYmRlNzg1YzUtZTNmYS00OGQ3LThhOGYtODc3NWYwMDZhYjIzIiwiYXR0cjEiOiIxIn0.iUSOfX74yU40AACGy8kpV3eNJBw6rQZ181rr2gv0hgY5eQSxki4DL-hpoZRRNX1Hs-pbjhHGIhYvgFmR596uWg"
reseller_client_identifier = "eyJhbGciOiJIUzUxMiJ9.eyJjbGllbnRJZGVudGlmaWVyIjoiNjlhNTllZDItYWM5OS00NzM0LTk5YTItYjNjMTgyNDZjOTM1OGNkM2I2ZTMtM2E0Mi00ZGIwLWE4ZmUtYjA4MGY4NDZkZmI4IiwiYXR0cjEiOiIxIn0.UO8z666UiYQzQFkI_d_bs3CjqIs8_u5kdM9nLplMTjL4bVy3zj38thMRitjjq6lhVfa6TaWAFiWGQFD0SFtLjQ"
customer_public_key = "MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQB5tYEcI0yfymdOKk2so71hjn0GqaJ5NSLEH9IBRUa0EPUOvvQdNN//RpqsKtgUazxpiS6ao6VgfrBhnF57LtHRq/Jgk1sgaoade9q7y+bUz0fjELxtYT0lFKvVyEQPb/G4dWvUP6CEPvKJbqsifdolsPGZjFbdRIQYD3bW122VT5Zs0uJCgul7XqeY8nSn7/N8fHTHPofvbBY9Rf/LPjlz6JI8o9EcZcuDHMq17yGzPq7XNgcHphJn+bfKt2PvSfRffQivVueCBrXj9NTFTaHPmGHo2U3Tlg0+x7BTYYyaq/HcKdNa8mbktsGT72ykP34W0mFsStOjJe66aEtTndtTAgMBAAE="
reseller_public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmbY9T6+i+zuch+1f7IWDuzzWtNl/J+dMuicwwaJJ1keq+qhusgoN4mWmG9BiMX0uOs0VxfqSTqwJutGW4Zd+kXRTApQRh+KCgTD5IxVztNxTlDKwLu+4JVt+XjYdYp4hLCwfRLOPGQmYVRrSdcxTXkWucvXtCkShKq7QdaxiF6AJyRXHi7bSWh9x30wWYanXwIfPVXEUJGxI5+mO/ayap4W3SAiKcmhz6YYINcW8pUXOkk8P0i1PhHLbnMvu0AYxZlGsYKShwEsyv+REp0VlQt8Z7dhCIHosGXrVd2EUENsydcIpNONhPHzmF0d6ugcrfaBjspgQDDninI2UV6sc/wIDAQAB"
customer_id = "1878142833"
reseller_id = "3378805019"
dem_client_key = "pSm!x6wlzcInpH7szkqe"
dem_client_secret = "h!kkvqtPB6PgJ*9tZtVT2bZ#k^"
sdk_auth_token_expiry_seconds = 120
#------------------------------------------------------------------------------------




def get_md5(input_text):
    try:
        return hashlib.md5(input_text.encode("utf-8")).hexdigest()
    except Exception:
        return None


BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))




