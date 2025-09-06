from time import time
from aiofiles import open
from msgspec import convert
from typing import Any, Literal

from aminodorks.utils import Endpoints, Crypt
from aminodorks.structures import AuthStructure

from aminodorks.services import (
    Singleton,
    AminoService,
    DorksService
)


class Client:
    def __init__(self, token: str) -> None:
        self._dorks_service: DorksService = DorksService(token)
        self._amino_service: AminoService = AminoService(self._dorks_service)

    @property
    def auid(self) -> str | None:
        return self._amino_service.headers_builder.auid

    @property
    def device_id(self) -> str:
        return self._amino_service.headers_builder.device_id

    @property
    def session_id(self) -> str | None:
        return self._amino_service.headers_builder.session_id

    @classmethod
    async def aclose(cls) -> None:
        await Singleton.aclose()

    @classmethod
    async def httpx_config(cls, config: dict[str, Any]):
        await Singleton.init_with_config(config)

    async def update_public_key(self, user_id: str) -> Any:
        return await self._amino_service.post(
            path=Endpoints.UPDATE_PUBLIC_KEY_PATH,
            data=Singleton.encode(await self._dorks_service.public_key_credentials(user_id))
        )

    async def authenticate_with_sid(self, session_id: str, device_id: str | None = None, update_public_key: bool = False) -> None:
        self._amino_service.headers_builder.update(
            session_id=session_id,
            device_id=device_id or Crypt.device_id(),
            auid=Crypt.auid_from_session_id(session_id),
        )

        if update_public_key: await self.update_public_key(self.auid)

    async def authenticate(self, email: str, password: str, update_public_key: bool = False) -> AuthStructure:
        payload: str = Singleton.encode({
            "email": email,
            "secret": f"0 {password}",
            "deviceID": self.device_id,
            "action": "normal",
            "v": 2,
            "clientType": 100,
            "timestamp": int(time() * 1000)
        })

        response = convert(await self._amino_service.post(path=Endpoints.LOGIN_PATH, data=payload), AuthStructure)
        self._amino_service.headers_builder.update(
            auid=response.auid,
            session_id=response.sid,
            device_id=self.device_id
        )

        if update_public_key: await self.update_public_key(response.auid)
        return response

    async def upload_media(self, file: str, file_type: Literal["audio/aac", "image/jpeg"]) -> str:
        async with open(file, "rb") as file:
            data = await file.read()

        response = await self._amino_service.post(
            path=Endpoints.UPLOAD_MEDIA_PATH, data=data,
            content_type=file_type
        )

        return response["mediaValue"]

__all__ = ["Client"]