from ..utils import Crypt, Headers
from ._dorks_service import DorksService


class HeadersBuilder:
    def __init__(self, dorks_service: DorksService) -> None:
        self._auid: str | None = None
        self._device_id: str | None = None
        self._session_id: str | None = None

        self._dorks_service: DorksService = dorks_service
        self._session_headers: dict[str, str] = Headers.AMINOAPPS_HEADERS.value

    @property
    def auid(self) -> str | None:
        return self._auid

    @property
    def device_id(self) -> str:
        if not self._device_id:
            self._device_id = Crypt.device_id()

        return self._device_id

    @property
    def session_id(self) -> str | None:
        return self._session_id

    @auid.setter
    def auid(self, value: str | None) -> None:
        self._auid = value

        if value:
            self._session_headers["auid"] = value
        else:
            self._session_headers.pop("auid", None)

    @device_id.setter
    def device_id(self, value: str | None) -> None:
        self._device_id = value

        if value:
            self._session_headers["ndcdeviceid"] = value
        else:
            self._session_headers.pop("ndcdeviceid", None)

    @session_id.setter
    def session_id(self, value: str | None) -> None:
        self._session_id = value

        if value:
            self._session_headers["ndcauth"] = f"sid={value}"
        else:
            self._session_headers.pop("ndcauth", None)

    def update(
        self,
        auid: str | None = None,
        device_id: str | None = None,
        session_id: str | None = None
    ) -> None:
        self.auid = auid
        self.device_id = device_id
        self.session_id = session_id

    async def build_headers(
        self,
        data: str | bytes | None = None,
        content_type: str | None = None
    ) -> dict[str, str]:
        headers: dict[str, str] = self._session_headers.copy()

        if content_type:
            headers["content-type"] = content_type

        if data:
            headers["ndc-msg-sig"] = Crypt.signature(data)

            if headers.get("auid") and not content_type:
                headers["ndc-message-signature"] = await self._dorks_service.ecdsa(headers["auid"], data)

        return headers
