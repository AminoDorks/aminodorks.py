from typing import Any
from msgspec import Struct


class Account(Struct, rename="camel"):
    nickname:       str
    username:       str | None
    modified_time:  str
    status:         int
    media_list:     list[Any] | None