from typing import Any
from urllib.parse import urljoin
from httpx import AsyncClient, Response

from ..utils import Hosts
from ._singleton import Singleton
from ._dorks_service import DorksService
from ._headers_builder import HeadersBuilder


class AminoService:
    def __init__(self, dorks_service: DorksService) -> None:
        self._headers_builder = HeadersBuilder(dorks_service)

    @property
    def instance(self) -> AsyncClient:
        return Singleton.instance()

    @property
    def headers_builder(self) -> HeadersBuilder:
        return self._headers_builder

    async def call(self, method: str, path: str, **kwargs: Any) -> Response:
        response = await self.instance.request(
            method=method,
            url=urljoin(Hosts.AMINOAPPS_API, path),
            headers=await self._headers_builder.build_headers(
                kwargs.get("data"), kwargs.pop("content_type", None)
            ),
            **kwargs
        )
        response.raise_for_status()

        return response

    async def post(self, path: str, **kwargs) -> dict[str, Any]:
        return Singleton.decode((await self.call("POST", path, **kwargs)).content)

    async def get(self, path: str, **kwargs) -> dict[str, Any]:
        return Singleton.decode((await self.call("GET", path, **kwargs)).content)

    async def delete(self, path: str, **kwargs) -> dict[str, Any]:
        return Singleton.decode((await self.call("DELETE", path, **kwargs)).content)

__all__ = ["AminoService"]