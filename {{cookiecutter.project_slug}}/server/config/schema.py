import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong!"


@strawberry.type
class Mutation(UserMutations):
    pass

schema = strawberry.Schema()
