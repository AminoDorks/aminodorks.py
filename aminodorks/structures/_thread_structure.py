from msgspec import Struct


class Thread(Struct, rename="camel"):
    uid:                str
    title:              str
    thread_id:          str
    content:            str | None
    icon:               str
    type:               int
    status:             int
    publish_to_global:  int
    ndc_id:             int
    members_count:      int


class ThreadStructure(Struct, rename="camel"):
    thread_list: list[Thread]

    @property
    def titles(self) -> list[str]:
        return [thread.title for thread in self.thread_list if thread.title]

    @property
    def thread_ids(self) -> list[str]:
        return [thread.thread_id for thread in self.thread_list if thread.thread_id]

__all__ = ["Thread", "ThreadStructure"]