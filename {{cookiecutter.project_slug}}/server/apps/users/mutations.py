import graphene
import graphql_jwt

from django.utils import timezone
from graphql_jwt.shortcuts import get_token
from guardian.shortcuts import assign_perm

from utils.graphql import get_user_from_info
from utils.resources import retrieve_resource
from utils.crypto import generate_reset_token
from utils.email import send_email_template

from apps.users.models import User
from apps.users.schema import UserType

from apps.auth.models import PasswordToken


class UserUpdateMutation(graphene.Mutation):
	class Arguments:
		pass

	success = graphene.Boolean()
	error = graphene.String()
	user = graphene.Field(UserType)

	def mutate(self, info, *args, **kwargs):
		pass


class ChangePasswordMutation(graphene.Mutation):
	class Arguments:
		old_password = graphene.String(required=True)
		new_password = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()
	user = graphene.Field(UserType)

	def mutate(self, info, *args, **kwargs):
		pass


class UserDeleteMutation(graphene.Mutation):
	class Arguments:
		pass

	success = graphene.Boolean()
	error = graphene.String()
	user = graphene.Field(UserType)

	def mutate(self, info, *args, **kwargs):
		pass


class UserMutations(graphene.ObjectType):
	update_user = UserUpdateMutation.Field()
	delete_user = UserDeleteMutation.Field()
	change_password = ChangePasswordMutation.Field()
