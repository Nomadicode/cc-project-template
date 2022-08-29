from .base import *
from .base import env

SECRET_KEY = env("DJANGO_SECRET")
DEBUG=env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="")

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# Your stuff...
# ------------------------------------------------------------------------------