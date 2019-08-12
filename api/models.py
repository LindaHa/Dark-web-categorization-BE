from typing import List


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
    members: List[Page]

    def __init__(self, **kwargs):
        for field in ("id", "links", "members"):
            setattr(self, field, kwargs.get(field, None))


class MetaGroup(object):
    id: str
    links: List[str]
    members_count: int

    def __init__(self, **kwargs):
        for field in ("id", "links", "members_count"):
            setattr(self, field, kwargs.get(field, None))
