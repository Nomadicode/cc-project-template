import graphene
import graphql_jwt

from django.utils import timezone
from graphql_jwt.shortcuts import get_token
from guardian.shortcuts import assign_perm

from utils.graphql import get_user_from_info
from utils.resources import retrieve_resource
from utils.crypto import generate_reset_token
from utils.email import send_email_template
from utils.messages import ErrorMessage

from apps.users.models import User
from apps.users.schema import UserType

from apps.auth.models import PasswordToken


class RegisterMutation(graphene.Mutation):
	class Arguments:
		first_name = graphene.String(required=True)
		last_name = graphene.String(required=True)
		email = graphene.String(required=True)
		password = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()
	user = graphene.Field(UserType)
	token = graphene.String()

	def mutate(self, info, *args, **kwargs):
		user = get_user_from_info(info)

		if user.is_authenticated:
			return RegisterMutation(
				success=False,
				error=ErrorMessage.LOGGED_IN,
				user=None,
				token=None
			)
		
		user, success = retrieve_resource(User, {'email': kwargs.get('email')})

		if success:
			return RegisterMutation(
				success=False,
				error=ErrorMessage.ACCOUNT_EXISTS,
				user=None,
				token=None
			)

		user = User.objects.create(**kwargs)
		user.set_password(kwargs.get('password'))
		user.save()

		assign_perm('change_user', user, user)
		assign_perm('delete_user', user, user)

		token = get_token(user)

		return RegisterMutation(
			success=True,
			error=None,
			user=user,
			token=token
		)


class LoginMutation(graphql_jwt.JSONWebTokenMutation):
	user = graphene.Field(UserType)

	@classmethod
	def resolve(cls, root, info, **kwargs):
		return cls(user=info.context.user)


class RecoverPasswordMutation(graphene.Mutation):
	class Arguments:
		email = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()

	def mutate(self, info, *args, **kwargs):
		user, success = retrieve_resource(User, {'email': kwargs.get('email')})

		if not success:
			return RecoverPasswordMutation(
				success=False,
				error=ErrorMessage.NO_ACCOUNT
			)
		
		token = generate_reset_token()
		recovery_token = PasswordToken.objects.create(user=user, token=token)

		reset_url = f"https://{}.com/account/reset-password/{recovery_token.token}"

		context = {
            "name": user.name,
            "reset_url": reset_url
        }
        
		send_email_template(
            f"Password Reset for {user.email}",
            "password_reset",
            [user.email, ],
            **context
        )
		
		# Send reset email
		return RecoverPasswordMutation(success=True, error=None)


class ResetPasswordMutation(graphene.Mutation):
	class Arguments:
		email = graphene.String(required=True)
		new_password = graphene.String(required=True)
		token = graphene.String(required=True)

	success = graphene.Boolean()
	error = graphene.String()

	def mutate(self, info, *args, **kwargs):
		user, success = retrieve_resource(User, {'email': kwargs.get('email')})

		if not success:
			return ResetPasswordMutation(
				success=False,
				error=ErrorMessage.NO_ACCOUNT
			)
		
		token, found_token = retrieve_resource(PasswordToken, {
			"user__pk": user.pk,
			"token": kwargs.get('token')
		})
		
		if not found_token:
			return ResetPasswordMutation(
				success=False,
				error=ErrorMessage.NO_TOKEN
			)

		current_date = timezone.now()

		total_seconds = (current_date - token.created_at).total_seconds()
		if total_seconds > 86400:
			token.delete()
			return ResetPasswordMutation(
				success=False,
				error=ErrorMessage.TOKEN_EXPIRED
			)
		    
		user.set_password(kwargs.get('new_password'))
		user.save()
		
		token.delete()

        # Send Email       
		context = {
            "name": user.name
        }
		send_email_template(
            f"Password update confirmation for {user.email}",
            "password_reset",
            [user.email, ],
            **context
        )
		
		# Send reset email
		return ResetPasswordMutation(success=True, error=None)


class AuthMutations(graphene.ObjectType):
	register = RegisterMutation.Field()
	login = LoginMutation.Field()
	recover_password = RecoverPasswordMutation.Field()
	reset_password = ResetPasswordMutation.Field()
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()
	revoke_token = graphql_jwt.Revoke.Field()
