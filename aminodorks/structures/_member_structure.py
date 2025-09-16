from msgspec import Struct


class Member(Struct, rename="camel"):
    icon:           str | None
    uid:            str
    nickname:       str
    role:           int
    reputation:     int


class MemberStructure(Struct, rename="camel"):
    member_list: list[Member]

__all__ = ["Member", "MemberStructure"]