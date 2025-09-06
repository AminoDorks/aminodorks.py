from hmac import new
from typing import Any
from hashlib import sha1
from orjson import loads
from functools import reduce
from secrets import token_bytes
from base64 import b64encode, b64decode

from ._constants import HmacKeys

class Crypt:
    @classmethod
    def signature(cls, data: str | bytes) -> str:
        if isinstance(data, str):
            data = data.encode("utf-8")

        digest = new(HmacKeys.SIGNATURE_KEY.value, data, sha1).digest()
        signed = HmacKeys.SALT.value[0:1] + digest
        return b64encode(signed).decode("utf-8")

    @classmethod
    def device_id(cls) -> str:
        random_bytes = token_bytes(20)
        data = HmacKeys.SALT.value + sha1(random_bytes).digest()

        digest = new(HmacKeys.DEVICE_KEY.value, data, sha1).hexdigest()
        return f"{data.hex()}{digest}".upper()

    @classmethod
    def decode_session_id(cls, session_id: str) -> dict[str, Any]:
        return loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), session_id + "=" * (-len(session_id) % 4)).encode())[1:-20].decode())

    @classmethod
    def auid_from_session_id(cls, session_id: str) -> str:
        return cls.decode_session_id(session_id)["2"]

__all__ = ["Crypt"]