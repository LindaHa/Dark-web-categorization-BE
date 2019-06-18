from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'pages', views.PageViewSet, base_name='tasks')

urlpatterns = router.urls
