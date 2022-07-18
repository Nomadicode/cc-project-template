from django.urls import include, re_path

from rest_framework import routers

from apps.users.views import UserViewSet

router = routers.SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    re_path(r'', include(router.urls))
]
