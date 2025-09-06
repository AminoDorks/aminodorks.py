from msgspec import Struct

from ._account import Account


class AuthStructure(Struct, rename="camel"):
    sid:        str
    auid:       str
    account:    Account

__all__ = ["AuthStructure"]