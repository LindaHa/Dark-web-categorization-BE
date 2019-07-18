class Page(object):
    def __init__(self, **kwargs):
        for field in ("id", "url", "content", "title", "links"):
            setattr(self, field, kwargs.get(field, None))


class Component(object):
    def __init__(self, **kwargs):
        for field in ("id", "members"):
            setattr(self, field, kwargs.get(field, None))


class Link(object):
    def __init__(self, **kwargs):
        for field in ("link", "name"):
            setattr(self, field, kwargs.get(field, None))
