from typing import List, Dict


class Link(object):
    name: str
    link: str

    def __init__(self, **kwargs):
        for field in ("link", "name"):
            setattr(self, field, kwargs.get(field, None))


class Page(object):
    id: str
    url: str
    content: str
    title: str
    links: List[Link]

    def __init__(self, **kwargs):
        for field in ("id", "url", "content", "title", "links"):
            setattr(self, field, kwargs.get(field, None))


class Group(object):
    id: str
    links: List[Link]
    members: Dict[str, Page]

    def __init__(self, **kwargs):
        for field in ("id", "links", "members"):
            setattr(self, field, kwargs.get(field, None))


NUMBER_OF_FIRST_MEMBERS = 10


class MetaGroup(object):
    id: str
    links: List[str]
    first_members: List[Page]
    members_count: int

    def __init__(self, **kwargs):
        for field in ("id", "links", "first_members", "members_count"):
            setattr(self, field, kwargs.get(field, None))
