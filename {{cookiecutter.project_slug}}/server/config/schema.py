import strawberry

from apps.users.schema import Query as UserQuery

from apps.users.mutations import Mutation as UserCreateMutation

@strawberry.type
class Query(UserQuery):
    @strawberry.field
    def ping(self) -> str:
        return "pong!"


@strawberry.type
class Mutation(UserCreateMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)