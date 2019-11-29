from typing import List, Dict


class Link(object):
    name: str
    link: str

    def __init__(self, **kwargs):
        for field in ("link", "name"):
            setattr(self, field, kwargs.get(field, None))


class Category(object):
    name: str
    occurrence: int

    def __init__(self, **kwargs):
        for field in ("name", "occurrence"):
            setattr(self, field, kwargs.get(field, None))


class Page(object):
    id: str
    url: str
    content: str
    title: str
    links: List[Link]
    categories: List[Category]

    def __init__(self, **kwargs):
        for field in ("id", "url", "content", "title", "links", "categories"):
            setattr(self, field, kwargs.get(field, None))


class Group(object):
    id: str
    links: List[Link]
    members: Dict[str, Page]
    categories: List[Category]

    def __init__(self, **kwargs):
        for field in ("id", "links", "members", "categories"):
            setattr(self, field, kwargs.get(field, None))


NUMBER_OF_FIRST_MEMBERS = 10


class MetaGroup(object):
    id: str
    links: List[str]
    first_members: List[Page]
    members_count: int
    categories: List[Category]

    def __init__(self, **kwargs):
        for field in ("id", "links", "first_members", "members_count", "categories"):
            setattr(self, field, kwargs.get(field, None))


class GroupDetails(object):
    members_urls: List[str]

    def __init__(self, **kwargs):
        for field in ["members_urls"]:
            setattr(self, field, kwargs.get(field, None))


class PageDetails(object):
    links: List[str]

    def __init__(self, **kwargs):
        for field in ["links"]:
            setattr(self, field, kwargs.get(field, None))
