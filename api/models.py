class Page(object):
    def __init__(self, **kwargs):
        for field in ('id', 'url', 'description', 'categories', 'linksTo'):
            setattr(self, field, kwargs.get(field, None))


# class Link(models.Model):
#     source = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='source')
#     target = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='target')
#
#     def __str__(self):
#         return self.id
