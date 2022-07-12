import graphene
from .models import User
from .schema import UserType

from utils.messages import Messages

class UserCreateMutation(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        user = None
        try:
            user = User.objects.get(email=kwargs['email'])
        except User.DoesNotExist:
            pass

        if user:
            return UserCreateMutation(success=False,
                                      error=Messages.USER_EMAIL_ALREADY_EXISTS,
                                      user=None)
        
        user_data = {
            "first_name": kwargs['first_name'],
            "last_name": kwargs['last_name'],
            "email": kwargs['email']
        }
        user = User(**kwargs).save()
        user.set_password(kwargs['password'])
        user.save()

        return UserCreateMutation(success=True, error=None, user=user)

class UserUpdateMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
    
    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            return UserUpdateMutation(success=False, 
                                      error=Messages.USER_NOT_FOUND, 
                                      user=None)
        user_data = {
            "first_name": kwargs['first_name'],
            "last_name": kwargs['last_name'],
            "email": kwargs['email']
        }

        for attr, value in user_data.items():
            setattr(user, attr, value)
        
        user.save()

        return UserUpdateMutation(success=True, error=None, user=user)


class UserDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=True)
    
    success = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            return UserDeleteMutation(success=False, 
                                      error=Messages.USER_NOT_FOUND)

        user.delete()

        return UserDeleteMutation(success=True, error=None)


class UserMutations(graphene.ObjectType):
    create_user = user_mutations.UserCreateMutation.Field()
    update_user = user_mutations.UserUpdateMutation.Field()
    delete_user = user_mutations.UserDeleteMutation.Field()
