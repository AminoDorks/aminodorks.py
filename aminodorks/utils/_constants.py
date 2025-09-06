from enum import StrEnum, Enum


class Hosts(StrEnum):
    AMINOAPPS_API = "https://service.aminoapps.com"
    DORKS_API = "https://qfhmflnp-3000.euw.devtunnels.ms"


class Headers(Enum):
    DORKS_HEADERS = {
        "connection": "keep-alive",
        "content-type": "application/json"
    }

    AMINOAPPS_HEADERS = {
        "connection": "keep-alive",
        "accept-language": "en-US",
        "host": "service.aminoapps.com",
        "content-type": "application/json",
        "user-agent": (
            "Dalvik/2.1.0 (Linux; U; Android 10; M2006C3MNG "
            "Build/QP1A.190711.020;com.narvii.amino.master/4.3.3121)"
        )
    }


class HmacKeys(Enum):
    SALT = bytes.fromhex("52")
    DEVICE_KEY = bytes.fromhex("AE49550458D8E7C51D566916B04888BFB8B3CA7D")
    SIGNATURE_KEY = bytes.fromhex("EAB4F1B9E3340CD1631EDE3B587CC3EBEDF1AFA9")


class Endpoints(StrEnum):
    LOGIN_PATH = "/api/v1/g/s/auth/login"
    UPLOAD_MEDIA_PATH = "/api/v1/g/s/media/upload"
    UPDATE_PUBLIC_KEY_PATH = "/api/v1/g/s/security/public_key"