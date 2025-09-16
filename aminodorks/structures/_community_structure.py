from msgspec import Struct


class Agent(Struct, rename="camel"):
    status:     int | None
    uid:        str | None
    level:      int | None
    ndc_id:     int | None
    nickname:   str | None


class Community(Struct, rename="camel"):
    ndc_id:             int | None
    link:               str | None
    icon:               str | None
    name:               str | None
    members_count:      int | None
    primary_language:   str | None
    agent:              Agent | None


class CommunityStructure(Struct, rename="camel"):
    community_list: list[Community]

    @property
    def names(self) -> list[str]:
        return [community.name for community in self.community_list if community.name]

    @property
    def ndc_ids(self) -> list[int]:
        return [community.ndc_id for community in self.community_list if community.ndc_id]

    def sort_by_language(self, lang: str) -> list[Community]:
        return [community for community in self.community_list if community.primary_language == lang]

    def sort_by_members_count(self, members_count: int) -> list[Community]:
        return [community for community in self.community_list if community.members_count >= members_count]

__all__ = [
    "Agent",
    "Community",
    "CommunityStructure"
]