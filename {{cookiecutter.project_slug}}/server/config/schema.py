import graphene

from apps.users.schema import Query as UserQuery

from apps.auth.schema import Query as AuthQuery
from apps.auth.mutations import AuthMutation


class RootQuery(graphene.ObjectType, AuthQuery, UserQuery):
    pass


class Mutations(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=RootQuery, mutation=Mutations)
