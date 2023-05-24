from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from decouple import config
# from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ChangeUserPasswordSerializer,
    UpdateUserSerializer,
    UserDetailSerializer,
)
from .models import CustomUser

# Create your views here.
CACHE_TTL = int(config("CACHE_TTL"))


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, *args, **kwargs):
        try:
            instance = CustomUser.objects.get(pk=request.user.id)
            serializer = UserDetailSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"status": "User Does Not Exist"}, status=status.HTTP_204_NO_CONTENT
            )


class RegisterUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(
                {"status": "User Info InComplete"}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutUserView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "Log out of all devices successful"})
        refresh_token = self.request.data.get("refresh_token")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "Log out Successful"})


class ChangePasswordView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUserPasswordSerializer


class UpdateUserview(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
