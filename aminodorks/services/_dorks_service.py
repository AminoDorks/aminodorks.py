from httpx import AsyncClient
from urllib.parse import urljoin

from ._singleton import Singleton
from ..utils import Hosts, Headers


class DorksService:
    def __init__(self, token: str) -> None:
        self._headers: dict[str, str] = {
            "Authorization": token,
            **Headers.DORKS_HEADERS.value
        }

    @property
    def instance(self) -> AsyncClient:
        return Singleton.instance()

    async def ecdsa(self, user_id: str, payload: str) -> str:
        response = await self.instance.request(
            method="POST",
            url=urljoin(Hosts.DORKS_API, "/api/v1/signature/ecdsa"),
            data=Singleton.encode({"userId": user_id, "payload": payload}), # type: ignore
            headers=self._headers
        )
        response.raise_for_status()

        return Singleton.decode(response.content)["ECDSA"]

    async def public_key_credentials(self, user_id: str) -> str:
        response = await self.instance.request(
            method="GET",
            headers=self._headers,
            url=urljoin(Hosts.DORKS_API, f"/api/v1/signature/credentials/{user_id}"),
        )
        response.raise_for_status()

        return Singleton.decode(response.content)["credentials"]

__all__ = ["DorksService"]