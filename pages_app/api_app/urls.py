from rest_framework import routers

from .views import PageViewSet

router = routers.DefaultRouter()
router.register('page', PageViewSet)
urlpatterns = router.urls
