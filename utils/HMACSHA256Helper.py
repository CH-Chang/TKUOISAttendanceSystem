import hmac
from base64 import b64encode
from hashlib import sha256

from configs.HMACSHA256Config import key

class HMACSHA256Helper:

    @staticmethod
    def HMACSHA256Hash(str):
        rawStr = str.encode('utf-8')
        rawKey = key.encode("utf-8")
        rawEncrypted = hmac.new(rawKey, rawStr, digestmod=sha256).digest()
        encrypted = b64encode(rawEncrypted).decode("utf-8")

        return encrypted

