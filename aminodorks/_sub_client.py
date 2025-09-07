from time import time
from typing import Literal
from msgspec import convert

from aminodorks.utils import Endpoints
from aminodorks.services import AminoService, Singleton

from aminodorks.structures import (
    Thread,
    UserProfileList,
    ThreadStructure,
    UserProfileStructure,
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

    async def invite_to_chat(self, user_ids: list[str], chat_id: str) -> int:
        response = await self._amino_service.post(
            path=Endpoints.INVITE_TO_CHAT.format(
                ndc_id=self._ndc_id, chat_id=chat_id
            ),
            data=Singleton.encode({
                "uids": user_ids,
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]

    async def get_chats(self, start: int = 0, size: int = 100) -> ThreadStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_JOINED_CHATS_PATH.format(
                    ndc_id=self._ndc_id, start=start, size=size
                )
            ), ThreadStructure)

    async def get_chat(self, chat_id: str) -> Thread:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_CHAT_PATH.format(
                    ndc_id=self._ndc_id, chat_id=chat_id
                )
            ), Thread)

    async def get_public_chats(
        self,
        start: int = 0,
        size: int = 100,
        chat_type: Literal["recommended", "hidden"] = "recommended"
    ) -> ThreadStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_PUBLIC_CHATS_PATH.format(
                    ndc_id=self._ndc_id, type=chat_type, start=start, size=size
                )
            ), ThreadStructure)

    async def send_message(
        self,
        chat_id: str,
        content: str,
        message_type: int = 0,
        mentioned_array: list[str] | None = None,
        reply_message_id: str | None = None
    ) -> int:
        response = await self._amino_service.post(
            path=Endpoints.ADD_MESSAGE_PATH.format(
                ndc_id=self._ndc_id, chat_id=chat_id
            ),
            data=Singleton.encode({
                "type": message_type,
                "content": content,
                "attachedObject": None,
                "clientRefId": 404354928,
                "uid": self._amino_service.headers_builder.auid,
                "extensions": {
                    "mentionedArray": mentioned_array or []
                },
                "replyMessageId": reply_message_id,
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]

__all__ = ["SubClient"]