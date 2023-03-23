from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from utils.messages import Message
from utils.responses import ApiResponse, ResponseType
from utils.resources import retrieve_resource

from apps.users.serializers import UserSerializer

User = get_user_model()

# Create your views here.
class UserViewSet(viewsets.ViewSet):
    def list(self, request): 
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return ApiResponse(ResponseType.RETRIEVED, data=serializer.data)

    def retrieve(self, request, username=None):
        user, success = retrieve_resource(User, 'username', username)

        if not success:
            return ApiResponse(
                ResponseType.NOT_FOUND,
                message=Message.NOT_FOUND.format("User", username)
            )

        serializer = UserSerializer(user)
        return ApiResponse(ResponseType.RETRIEVED, data=serializer.data)

    def update(self, request, username=None):
        if not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        user, success = retrieve_resource(User, 'username', username)

        if not success:
            return ApiResponse(
                ResponseType.NOT_FOUND,
                message=Message.NOT_FOUND.format("User", username)
            )

        if not request.user.has_perm('change_user', user):
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )
        
        serializer = UserSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return ApiResponse(
                ResponseType.INVALID,
                data={
                    "errors": serializer.errors
                }
            )
        
        serializer.save()
        return ApiResponse(
            ResponseType.UPDATED,
            data=serializer.data
        )

    def update_password(self, request):
        if not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        if not request.user.has_perm('change_user', request.user):
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        if not request.user.check_password(request.data.get('current_password')):
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )
        
        request.user.set_password(request.data.get('new_password'))
        request.user.save()

        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            pass

        if token:
            token.delete()

        return ApiResponse(
            ResponseType.UPDATED,
            message="Password Updated"
        )

    def destroy(self, request, username=None):
        if not request.user.is_authenticated:
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )

        user, success = retrieve_resource(User, 'username', username)

        if not success:
            return ApiResponse(
                ResponseType.NOT_FOUND,
                message=Message.NOT_FOUND.format("User", username)
            )
        
        if not request.user.has_perm('delete_user', user):
            return ApiResponse(
                ResponseType.UNAUTHORIZED,
                message=Message.NOT_AUTHORIZED
            )
        
        user.delete()

        return ApiResponse(
            ResponseType.DESTROYED,
            message=Message.RESOURCE_DESTROYED.format("User", user.pk)
        )
