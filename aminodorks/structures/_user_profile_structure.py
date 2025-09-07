from typing import Any
from msgspec import Struct


class UserProfile(Struct, rename="camel"):
    status:                     int
    items_count:                int
    reputation:                 int
    uid:                        str
    consecutiveCheckInDays:     Any | None
    mood_sticker:               Any | None


class UserProfileStructure(Struct, rename="camel"):
    user_profile: UserProfile

    @property
    def auid(self) -> str:
        return self.user_profile.uid


class UserProfileList(Struct, rename="camel"):
    user_profile_list: list[UserProfile]


__all__ = [
    "UserProfile",
    "UserProfileList",
    "UserProfileStructure"
]