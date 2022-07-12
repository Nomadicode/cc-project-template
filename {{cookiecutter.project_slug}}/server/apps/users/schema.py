import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType

from .models import User


class UserType(DjanogObjectType):
    pk = graphene.ID()

    class Meta:
        model = User
        exclude_fields = ('password',)


class UserConnection(relay.Connection):
    class Meta:
        node = UserType


class UserQuery(object):
    user = graphene.Field(UserType, pk=graphene.ID(required=True))
    users = relay.ConnectionField(UserConnection, is_staff=graphene.Boolean())

