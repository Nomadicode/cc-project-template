from django.conf.urls import include, url

from rest_framework import routers

from apps.users.views import UserViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    url(r'', include(router.urls))
]
