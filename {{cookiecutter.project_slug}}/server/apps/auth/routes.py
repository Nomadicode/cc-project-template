from django.conf.urls import include
from django.urls import re_path

from rest_framework import routers

from apps.auth.views import AuthViewset

router = routers.SimpleRouter()
router.register('auth', AuthViewset)

urlpatterns = [
    re_path(r'', include(router.urls)),
]
