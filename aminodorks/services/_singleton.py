from typing import Any
from httpx import AsyncClient
from msgspec.json import Decoder, Encoder


class Singleton:
    _encoder = Encoder()
    _decoder = Decoder()
    _instance: AsyncClient | None = None

    @classmethod
    def encode(cls, obj: Any) -> str:
        return cls._encoder.encode(obj).decode("utf-8")

    @classmethod
    def decode(cls, obj: Any) -> dict[str, Any]:
        return cls._decoder.decode(obj)

    @classmethod
    def instance(cls) -> AsyncClient:
        if not cls._instance:
            cls._instance = AsyncClient()

        return cls._instance

    @classmethod
    async def aclose(cls) -> None:
        if cls._instance and not cls._instance.is_closed:
            await cls._instance.aclose()

        cls._instance = None

    @classmethod
    async def init_with_config(cls, config: dict[str, Any]) -> AsyncClient:
        if "base_url" in config:
            raise ValueError("Base URL can not be provided!")
        
        if cls._instance:
            await cls.aclose()

        cls._instance = AsyncClient(**config)
        return cls._instance

__all__ = ["Singleton"]