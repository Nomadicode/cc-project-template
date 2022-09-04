import strawberry
from typing import List
from .types import UserType

@strawberry.type
class Query:
    users: List[UserType] = strawberry.django.field()
