from time import time
from aiofiles import open
from msgspec import convert
from typing import Any, Literal

from ._sub_client import SubClient
from aminodorks.utils import Endpoints, Crypt

from aminodorks.services import (
    Singleton,
    AminoService,
    DorksService
)

from aminodorks.structures import (
    AuthStructure,
    UserProfileList,
    LinkInfoStructure,
    CommunityStructure,
    UserProfileStructure
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
    async def httpx_config(cls, config: dict[str, Any]) -> None:
        await Singleton.init_with_config(config)

    @classmethod
    def format_media(cls, media: str | None) -> list[list[int | str | None]] | None:
        return [[100, media, None]] if media else None

    def sub_client(self, ndc_id: int | str) -> SubClient:
        return SubClient(ndc_id, self._amino_service)

    async def upload_media(self, file: str, file_type: Literal["audio/aac", "image/jpeg"]) -> str:
        async with open(file, "rb") as file:
            data = await file.read()

        response = await self._amino_service.post(
            path=Endpoints.UPLOAD_MEDIA_PATH, data=data,
            content_type=file_type
        )

        return response["mediaValue"]

    async def update_public_key(self, user_id: str) -> Any:
        return await self._amino_service.post(
            path=Endpoints.UPDATE_PUBLIC_KEY_PATH,
            data=Singleton.encode(await self._dorks_service.public_key_credentials(user_id))
        )

    async def authenticate_with_sid(self, session_id: str, device_id: str | None = None, update_public_key: bool = True) -> None:
        self._amino_service.headers_builder.update(
            session_id=session_id,
            device_id=device_id or Crypt.device_id(),
            auid=Crypt.auid_from_session_id(session_id),
        )

        if update_public_key: await self.update_public_key(self.auid)

    async def authenticate(self, email: str, password: str, update_public_key: bool = True) -> AuthStructure:
        response = convert(
            await self._amino_service.post(
                path=Endpoints.LOGIN_PATH,
                data=Singleton.encode({
                    "email": email,
                    "secret": f"0 {password}",
                    "deviceID": self.device_id,
                    "action": "normal",
                    "v": 2,
                    "clientType": 100,
                    "timestamp": int(time() * 1000)
                })
            ),
            AuthStructure
        )

        self._amino_service.headers_builder.update(
            auid=response.auid,
            session_id=response.sid,
            device_id=self.device_id
        )

        if update_public_key: await self.update_public_key(response.auid)
        return response

    async def link_resolution(self, link: str) -> LinkInfoStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.LINK_RESOLUTION_PATH.format(
                    link=link
                )
            ), LinkInfoStructure)

    async def join_community(self, ndc_id: int, invitation_id: str | None = None) -> int:
        payload: dict[str, Any] = {"timestamp": int(time() * 1000)}
        if invitation_id: payload["invitationId"] = invitation_id

        response = await self._amino_service.post(
            path=Endpoints.JOIN_COMMUNITY_PATH.format(
                ndc_id=f"x{ndc_id}"
            ),
            data=Singleton.encode(payload)
        )

        return response["api:statuscode"]

    async def leave_community(self, ndc_id: int) -> int:
        response = await self._amino_service.post(
            path=Endpoints.LEAVE_COMMUNITY_PATH.format(
                ndc_id=f"x{ndc_id}"
            ),
            content_type="application/x-www-form-urlencoded"
        )

        return response["api:statuscode"]

    async def get_user(self, user_id: str) -> UserProfileStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_USER_PATH.format(
                    ndc_id="g", user_id=user_id
                )
            ), UserProfileStructure)

    async def get_users(
        self,
        start: int = 0,
        size: int = 100,
        user_type: Literal[
            "recent", "banned",
            "featured", "leaders", "curators"] = "recent"
    ) -> UserProfileList:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_USERS_PATH.format(
                    ndc_id="g", type=user_type, start=start, size=size
                )
            ), UserProfileList)

    async def edit_profile(
        self,
        nickname: str | None = None,
        avatar: str | None = None,
        about: str | None = None,
        background_media_list: str | None = None,
        background_color: str | None = None
    ) -> int:
        response = await self._amino_service.post(
            path=Endpoints.EDIT_USER_PROFILE_PATH.format(
                ndc_id="g", auid=self.auid
            ),
            data=Singleton.encode({
                "nickname": nickname,
                "icon": avatar,
                "content": about,
                "extensions": {
                    "style": {
                        "backgroundMediaList": self.format_media(background_media_list),
                        "backgroundColor": background_color
                    }
                },
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]

    async def get_joined_communities(self, start: int = 0, size: int = 100) -> CommunityStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.JOINED_COMMUNITIES_PATH.format(
                    start=start, size=size
                )
            ), CommunityStructure
        )

__all__ = ["Client"]