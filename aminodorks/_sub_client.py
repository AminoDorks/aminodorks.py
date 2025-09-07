from typing import Literal
from msgspec import convert

from aminodorks.utils import Endpoints
from aminodorks.services import AminoService

from aminodorks.structures import (
    UserProfileList,
    UserProfileStructure
)


class SubClient:
    def __init__(self, ndc_id: int | str, amino_service: AminoService) -> None:
        self._ndc_id: int | str = f"x{ndc_id}"
        self._amino_service: AminoService = amino_service

    async def get_user(self, user_id: str) -> UserProfileStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_USER_PATH.format(
                    ndc_id=self._ndc_id, user_id=user_id
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
                    ndc_id=self._ndc_id, type=user_type, start=start, size=size
                )
            ), UserProfileList)

    async def get_online_users(self, start: int = 0, size: int = 100) -> UserProfileList:
        return convert(
            await self._amino_service.get(
                path=Endpoints.ONLINE_MEMBERS_PATH.format(
                    ndc_id=self._ndc_id, start=start, size=size
                )
            ), UserProfileList)

    async def join_chat(self, chat_id: str) -> int:
        response = await self._amino_service.post(
            path=Endpoints.JOIN_LEAVE_CHAT_PATH.format(
                ndc_id=self._ndc_id, chat_id=chat_id,
                user_id=self._amino_service.headers_builder.auid
            ),
            content_type="application/x-www-form-urlencoded"
        )

        return response["api:statuscode"]

    async def leave_chat(self, chat_id: str) -> int:
        response = await self._amino_service.delete(
            path=Endpoints.JOIN_LEAVE_CHAT_PATH.format(
                ndc_id=self._ndc_id, chat_id=chat_id,
                user_id=self._amino_service.headers_builder.auid
            ),
            content_type="application/x-www-form-urlencoded"
        )

        return response["api:statuscode"]