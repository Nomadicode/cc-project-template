import graphene

from apps.auth.mutations import AuthMutations
from apps.users.mutations import UserMutations


class RootQuery(
    graphene.ObjectType
):
    ping = graphene.Field(graphene.String)

    def resolve_ping(_, info):
        return "pong"


class Mutations(
    AuthMutations,
    UserMutations,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=RootQuery, mutation=Mutations)
