import base64
import random
import string
from django.contrib.auth.models import AnonymousUser

from apps.users.models import User


def get_user_from_info(info):
    jwt = info.context.META.get('HTTP_AUTHORIZATION', None)
    if jwt:
        jwt = jwt.split(' ')[-1]
        return User.decode_jwt(jwt)
    return AnonymousUser()

