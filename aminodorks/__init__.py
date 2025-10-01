__author__: str = "Nullable-developer"
__version__: str = "0.0.1b3"
__licence__: str = "MIT"

from ._client import Client
from ._sub_client import SubClient

from .structures import (
    AuthStructure,
    LinkInfoStructure,
    CommunityStructure,
    ThreadStructure, Thread,
    MemberStructure, Member,
    UserProfileStructure, UserProfileList
)

__all__ = [
    "Client",
    "SubClient",
    "AuthStructure",
    "LinkInfoStructure",
    "CommunityStructure",
    "ThreadStructure", "Thread",
    "MemberStructure", "Member",
    "UserProfileStructure", "UserProfileList"
]