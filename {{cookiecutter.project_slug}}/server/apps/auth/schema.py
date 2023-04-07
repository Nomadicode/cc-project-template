import graphene

from graphql_auth.schema import UserQuery
from graphql_auth import mutations


class Query(UserQuery, graphene.ObjectType):
   pass
