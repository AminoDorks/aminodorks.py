from time import time
from typing import Literal
from msgspec import convert

from aminodorks.utils import Endpoints
from aminodorks.services import AminoService, Singleton

from aminodorks.structures import (
    Thread,
    UserProfileList,
    ThreadStructure,
    UserProfileStructure, MemberStructure,
)


class SubClient:
    def __init__(self, ndc_id: int | str, amino_service: AminoService) -> None:
        self._ndc_id: int | str = f"x{ndc_id}"
        self._amino_service: AminoService = amino_service

    @property
    def auid(self) -> str | None:
        if self._amino_service.headers_builder.auid:
            return self._amino_service.headers_builder.auid

        raise Exception("You must be logged in to use this feature.")

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
                ndc_id=self._ndc_id, auid=self.auid
            ),
            data=Singleton.encode({
                "nickname": nickname,
                "icon": avatar,
                "content": about,
                "extensions": {
                    "style": {
                        "backgroundMediaList": [[100, background_media_list, None]] if background_media_list else None,
                        "backgroundColor": background_color
                    }
                },
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]


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
                "uid": self.auid,
                "extensions": {
                    "mentionedArray": mentioned_array or []
                },
                "replyMessageId": reply_message_id,
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]

    async def kick(self, user_id: str, chat_id: str, allow_rejoin: bool = False) -> int:
        response = await self._amino_service.delete(
            path=Endpoints.KICK_FROM_CHAT_PATH.format(
                ndc_id=self._ndc_id, chat_id=chat_id,
                user_id=user_id, allow_rejoin=allow_rejoin
            )
        )

        return response["api:statuscode"]

    async def get_following(self, user_id: str, start: int = 0, size: int = 100) -> UserProfileList:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_FOLLOWING_PATH.format(
                    ndc_id=self._ndc_id, user_id=user_id,
                    start=start, size=size
                )
            ), UserProfileList)

    async def get_followers(self, user_id: str, start: int = 0, size: int = 100) -> UserProfileList:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_FOLLOWERS_PATH.format(
                    ndc_id=self._ndc_id, user_id=user_id,
                    start=start, size=size
                )
            ), UserProfileList)

    async def get_chat_users(self, chat_id: str, start: int = 0, size: int = 100) -> MemberStructure:
        return convert(
            await self._amino_service.get(
                path=Endpoints.GET_CHAT_USERS_PATH.format(
                    ndc_id=self._ndc_id, chat_id=chat_id, start=start, size=size
                )
            ), MemberStructure)

    async def apply_frame(self, frame_id: str, apply_to_all: bool = False) -> int:
        response = await self._amino_service.post(
            path=Endpoints.APPLY_FRAME_PATH.format(
                ndc_id=self._ndc_id
            ),
            data=Singleton.encode({
                "frameId": frame_id,
                "applyToAll": int(apply_to_all),
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]

    async def get_block_list(self) -> list[str]:
        response = await self._amino_service.get(
            path=Endpoints.GET_BLOCK_LIST.format(
                ndc_id=self._ndc_id
            )
        )

        return response["blockedUidList"]

    async def follow(self, user_id: str) -> int:
        response = await self._amino_service.post(
            path=Endpoints.FOLLOW_PATH.format(
                ndc_id=self._ndc_id, user_id=user_id
            ),
            content_type="application/x-www-form-urlencoded"
        )

        return response["api:statuscode"]

    async def follow_list(self, user_ids: list[str]) -> int:
        response = await self._amino_service.post(
            path=Endpoints.FOLLOW_LIST_PATH.format(
                ndc_id=self._ndc_id, user_id=self.auid
            ),
            data=Singleton.encode({
                "targetUidList": user_ids,
                "timestamp": int(time() * 1000)
            })
        )

        return response["api:statuscode"]

    async def unfollow(self, user_id: str) -> int:
        response = await self._amino_service.delete(
            path=Endpoints.UNFOLLOW_PATH.format(
                ndc_id=self._ndc_id, auid=self.auid, user_id=user_id
            )
        )

        return response["api:statuscode"]

__all__ = ["SubClient"]