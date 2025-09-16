from enum import StrEnum, Enum


class Hosts(StrEnum):
    AMINOAPPS_API = "https://service.aminoapps.com"
    DORKS_API = "https://aminodorks.agency"


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
    # Only for client
    LOGIN_PATH = "/api/v1/g/s/auth/login"
    UPLOAD_MEDIA_PATH = "/api/v1/g/s/media/upload"
    UPDATE_PUBLIC_KEY_PATH = "/api/v1/g/s/security/public_key"
    LINK_RESOLUTION_PATH = "/api/v1/g/s/link-resolution?q={link}"
    JOIN_COMMUNITY_PATH = "/api/v1/{ndc_id}/s/community/join"
    LEAVE_COMMUNITY_PATH = "/api/v1/{ndc_id}/s/community/leave"
    JOINED_COMMUNITIES_PATH = "/api/v1/g/s/community/joined?v=1&start={start}&size={size}"

    # For client and sub client
    GET_USER_PATH = "/api/v1/{ndc_id}/s/user-profile/{user_id}"
    GET_USERS_PATH = "/api/v1/{ndc_id}/s/user-profile?type={type}&start={start}&size={size}"
    EDIT_USER_PROFILE_PATH = "/api/v1/{ndc_id}/s/user-profile/{auid}"
    GET_FOLLOWING_PATH = "/api/v1/{ndc_id}/s/user-profile/{user_id}/joined?start={start}&size={size}"
    APPLY_FRAME_PATH = "/api/v1/{ndc_id}/s/avatar-frame/apply`"
    GET_FOLLOWERS_PATH = "/api/v1/{ndc_id}/s/user-profile/{user_id}/member?start={start}&size={size}"
    GET_BLOCK_LIST = "/api/v1/{ndc_id}/s/block/full-list"
    FOLLOW_PATH = "/api/v1/{ndc_id}/s/user-profile/{user_id}/member"
    FOLLOW_LIST_PATH = "/api/v1/{ndc_id}/s/user-profile/{user_id}/joined"
    UNFOLLOW_PATH = "/api/v1/{ndc_id}/s/user-profile/{auid}/joined/{user_id}"

    # Only for sub client
    CHAT_PATH = "/api/v1/{ndc_id}/s/chat/thread"
    GET_CHAT_PATH = CHAT_PATH + "/{chat_id}"
    ADD_MESSAGE_PATH = CHAT_PATH + "/{chat_id}/message"
    JOIN_LEAVE_CHAT_PATH = CHAT_PATH + "/{chat_id}/member/{user_id}"
    GET_JOINED_CHATS_PATH = CHAT_PATH + "?type=joined-me&start={start}&size={size}"
    GET_PUBLIC_CHATS_PATH = CHAT_PATH + "?type=public-all&filterType={type}&start={start}&size={size}"
    INVITE_TO_CHAT = "/api/v1/{ndc_id}/s/chat/thread/{chat_id}/member/invite"
    ONLINE_MEMBERS_PATH = "/api/v1/{ndc_id}/s/live-layer?topic=ndtopic:{ndc_id}:online-members&start={start}&size={size}"
    KICK_FROM_CHAT_PATH = "/api/v1/{ndc_id}/s/chat/thread/{chat_id}/member/{user_id}?allowRejoin={allow_rejoin}"
    GET_CHAT_USERS_PATH = "/api/v1/{ndc_id}/s/chat/thread/{chat_id}/member?start={start}&size={size}&type=default&cv=1.2"

__all__ = [
    "Hosts",
    "Headers",
    "HmacKeys",
    "Endpoints"
]
