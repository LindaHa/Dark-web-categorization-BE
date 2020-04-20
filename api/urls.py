from rest_framework import routers

from . import view_sets

router = routers.DefaultRouter()

router.register(r'pages/bylink', view_sets.GroupsByLinkViewSet, base_name='tasks')
router.register(r'pages/bycategory', view_sets.GroupsByCategoryViewSet, base_name='tasks')
router.register(r'details/group', view_sets.GroupDetailsViewSet, base_name='tasks')
router.register(r'details/page', view_sets.PageDetailsViewSet, base_name='tasks')

urlpatterns = router.urls
