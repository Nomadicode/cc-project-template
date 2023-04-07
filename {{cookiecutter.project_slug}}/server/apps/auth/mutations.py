import graphene

from graphql_auth import mutations


class AuthMutation(graphene.ObjectType):
   register = mutations.Register.Field() #predefined settings to register user
   verify_account = mutations.VerifyAccount.Field() #used to verify account
   token_auth = mutations.ObtainJSONWebToken.Field() # get jwt to log in
