import graphene

from graphene_django.types import DjangoObjectType

from apps.users.models import User


class UserType(DjangoObjectType):
    pk = graphene.ID()

    class Meta:
        model = User
        exclude_fields = ('password', )


class UserQuery(graphene.AbstractType):
    user = graphene.Field(UserType, jwt=graphene.String(), pk=graphene.ID())

    def resolve_user(self, info, **kwargs):
        if 'pk' in kwargs: 
            return User.objects.get(pk=kwargs['pk'])
        
        jwt = info.context.META.get('HTTP_AUTHORIZATION', None)
        if jwt:
            jwt = jwt.split(' ')[-1]
            return User.decode_jwt(jwt)

        return User.decode_jwt(kwargs.get('jwt', ''))