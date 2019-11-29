from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'pages/bylink', views.GroupsByLinkViewSet, base_name='tasks')
router.register(r'pages/bycategory', views.GroupsByCategoryViewSet, base_name='tasks')
router.register(r'details/group', views.GroupDetailsViewSet, base_name='tasks')
router.register(r'details/page', views.PageDetailsViewSet, base_name='tasks')

urlpatterns = router.urls
