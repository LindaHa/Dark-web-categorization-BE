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


class PageDetails(object):
    url: str
    title: str or None
    category: str or None
    content: str or None
    links: List[str] or None

    def __init__(self, **kwargs):
        for field in ("url", "title", "category", "content", "links"):
            setattr(self, field, kwargs.get(field, None))


class DetailsOptions(object):
    title: bool
    category: bool
    content: bool
    links: bool

    def __init__(self, **kwargs):
        for field in ("title", "category", "content", "links"):
            setattr(self, field, kwargs.get(field, None))
