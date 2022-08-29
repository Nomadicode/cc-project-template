import strawberry
from strawberry import auto
from typing import List

from . import models

@strawberry.django.type(models.User)
class User:
    id: auto
    name: auto
    