from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.users.serializers import UserSerializer

User = get_user_model()

# Create your views here.
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminOrOwner, ]

    @action(detail=False, methods=["GET"])
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={
                    "status": "error",
                    "message": "You are not allowed to access that resource"
                }
            )
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(
            status=status.HTTP_200_OK,
            data={
                "status": "success",
                "data": {
                    "user": serializer.data
                }
            }
        )