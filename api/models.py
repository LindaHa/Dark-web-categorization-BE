from typing import List, Dict


class Link(object):
    link: str
    occurrences: int

    def __init__(self, **kwargs):
        for field in ("link", "occurrences"):
            setattr(self, field, kwargs.get(field, None))


class Category(object):
    name: str
    occurrence: int

    def __init__(self, **kwargs):
        for field in ("name", "occurrence"):
            setattr(self, field, kwargs.get(field, None))


class Page(object):
    url: str
    content: str
    title: str
    links: List[Link]
    categories: List[Category]
    last_updated: str

    def __init__(self, **kwargs):
        for field in ("url", "content", "title", "links", "categories", "last_updated"):
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
    links: List[Link]
    first_members: List[Page]
    members_count: int
    domains_count: int
    categories: List[Category]

    def __init__(self, **kwargs):
        for field in ("id", "links", "first_members", "members_count", "domains_count", "categories"):
            setattr(self, field, kwargs.get(field, None))


class PageDetails(object):
    url: str
    title: str or None
    category: str or None
    content: str or None
    last_updated: str or None
    links: List[str] or None

    def __init__(self, **kwargs):
        for field in ("url", "title", "category", "content", "links", "last_updated"):
            setattr(self, field, kwargs.get(field, None))


class DetailsOptions(object):
    title: bool
    category: bool
    content: bool
    last_updated: bool
    links: bool

    def __init__(self, **kwargs):
        for field in ("title", "category", "content", "links", "last_updated"):
            setattr(self, field, kwargs.get(field, None))


class FilterOptions(object):
    content: bool
    url: bool

    def __init__(self, **kwargs):
        for field in ("content", "url"):
            setattr(self, field, kwargs.get(field, None))
