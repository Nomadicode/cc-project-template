from strawberry import auto
from strawberry_django_plus import gql

from apps.users import models

@gql.django.type(models.User)
class UserType:
    id: auto
    first_name: auto
    last_name: str
    email: str
