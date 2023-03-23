from django.urls import path

from apps.users.views import UserViewSet

urlpatterns = [
    path('users/password/', UserViewSet.as_view({
        'put': 'update_password'
    })),
    path('users/<slug:username>/', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('users/', UserViewSet.as_view({
        'get': 'list'
    }))
]
