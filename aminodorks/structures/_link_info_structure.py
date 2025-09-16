from msgspec import Struct, field


class LinkInfo(Struct, rename="camel"):
    object_id:      str | None = field(default=None)
    target_code:    int | None = field(default=None)
    ndc_id:         int | None = field(default=None)
    object_type:    int | None = field(default=None)
    full_path:      str | None = field(default=None)


class Extensions(Struct, rename="camel"):
    link_info: LinkInfo | None = field(default_factory=LinkInfo)


class LinkInfoV2(Struct, rename="camel"):
    path:           str
    extensions:     Extensions | None = field(default_factory=Extensions)


class LinkInfoStructure(Struct, rename="camel"):
    link_info_v2: LinkInfoV2

    @property
    def ndc_id(self) -> int:
        return self.link_info_v2.extensions.link_info.ndc_id

    @property
    def object_id(self) -> str:
        return self.link_info_v2.extensions.link_info.object_id

    @property
    def path(self) -> str:
        return self.link_info_v2.path

__all__ = [
    "LinkInfo",
    "LinkInfoV2",
    "Extensions",
    "LinkInfoStructure"
]