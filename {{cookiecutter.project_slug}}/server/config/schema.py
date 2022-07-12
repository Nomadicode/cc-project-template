import graphene

from apps.users.schema import UserQuery
from apps.users.mutations import UserMutations

class Query(graphene.ObjectType):
    ping = graphene.String(default_value="pong!")


class Mutations(graphene.ObjectType, UserMutations):
    pass

schema = graphene.Schema(query=RootQuery, mutation=Mutations)