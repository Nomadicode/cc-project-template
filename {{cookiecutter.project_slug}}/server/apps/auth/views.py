from django.utils import timezone

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from guardian.shortcuts import assign_perm

from django.contrib.auth import authenticate, get_user_model

from utils.email import send_email_template

from apps.users.serializers import UserSerializer
from utils.messages import Message
from utils.responses import ApiResponse, ResponseType
from utils.resources import retrieve_resource, retrieve_resource_multiple_param

from apps.auth.models import PasswordToken

User = get_user_model()


# Create your views here.
class AuthViewset(GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()

    @action(detail=False, methods=['POST'])
    def register(self, request):
        if request.user.is_authenticated:
            return ApiResponse(
                ResponseType.INVALID,
                message=Message.ALREADY_SIGNED_IN
            )

        _, success = retrieve_resource(User, 'email', request.data.get('email'))
        
        if success:
            return ApiResponse(
                ResponseType.INVALID,
                message=Message.ACCOUNT_EXISTS
            )
        
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return ApiResponse(
                ResponseType.INVALID,
                data=serializer.errors
            )

        instance = serializer.save()       
        instance.set_password(request.data.get('password'))

        assign_perm('change_user', instance, instance)
        assign_perm('delete_user', instance, instance)

        instance.save()

        token, _ = Token.objects.get_or_create(user=instance)

        return ApiResponse(
            ResponseType.CREATED,
            data={
                "user": serializer.data,
                "token": token.key
            }
        )


    @action(detail=False, methods=['POST'])
    def login(self, request):
        if request.user.is_authenticated:
            return ApiResponse(
                ResponseType.INVALID,
                message=Message.ALREADY_SIGNED_IN
            )
        
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(email=email, password=password)

        if user is None:
             return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        serializer = UserSerializer(user)

        token, created = Token.objects.get_or_create(user=user)

        return ApiResponse(
            ResponseType.RETRIEVED,
            data={
                "user": serializer.data,
                "token": token.key
            }
        )

    @action(detail=False, methods=['POST'], url_path=r'password/forgot')
    def forgot_password(self, request):
        if request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.ALREADY_SIGNED_IN
            )
        
        email = request.data.get('email', None)

        user, success = retrieve_resource(User, 'email', email)

        if not success:
            return ApiResponse(
                ResponseType.NOT_FOUND,
                message=Message.NOT_FOUND.format('User', email)
            )

        reset_token = PasswordToken(user=user)
        reset_token.save()

        reset_url = f"https://example.com/account/password/reset/{reset_token.token}"

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

        return ApiResponse(
            ResponseType.CREATED,
            message=Message.PASSWORD_MESSAGE_SENT
        )

    @action(detail=False, methods=['POST'], url_path=r'password/reset')
    def reset_password(self, request):
        if request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.ALREADY_SIGNED_IN
            )

        token = request.data.get('token', None)
        email = request.data.get('email', None)
        new_password = request.data.get('password', None)

        user, success = retrieve_resource(User, 'email', email)

        if not success:
            return ApiResponse(
                ResponseType.NOT_FOUND,
                message=Message.NOT_FOUND.format('User', email)
            )

        reset_token, success = retrieve_resource_multiple_param(PasswordToken, {
            "email": email,
            "user__pk": user.pk
        })

        if not success:
            return ApiResponse(ResponseType.UNAUTHORIZED)

        current_date = timezone.now()
        
        total_seconds = (current_date - reset_token.created_at).total_seconds()
        if total_seconds > 86400:
            reset_token.delete()
            return ApiResponse(ResponseType.UNAUTHORIZED)

        user.set_password(new_password)
        user.save()

        reset_token.delete()

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

        return ApiResponse(
            ResponseType.RETRIEVED,
            message=Message.PASSWORD_RESET_SUCCESS
        )
