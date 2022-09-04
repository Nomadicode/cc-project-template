import strawberry

from apps.users.models import User
from apps.users.types import UserType


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str
    ) -> UserType:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        new_user.set_password(password)

        new_user.save()

        return new_user