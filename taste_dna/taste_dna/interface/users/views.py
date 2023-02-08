from django.contrib.auth import authenticate

# django imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

# app imports

from taste_dna.application.users.services import UserAppServices

# local imports
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status

class BadRequest(APIException):
    status_code = 400
    default_detail = (
        "The request cannot be fulfilled, please try again with different parameters."
    )
    default_code = "bad_request"


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = UserAppServices().list_users().order_by("?")
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "login":
            return UserLoginSerializer
        return UserSerializer

    @action(detail=False, methods=["post"], name="login")
    def login(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            email = serializer_data.data.get("email", None)
            password = serializer_data.data.get("password", None)
            try:
                user = authenticate(email=email, password=password)
                response_data = UserAppServices().get_user_token(user=user)
                return Response(response_data, status.HTTP_200_OK)
            except Exception as e:
                data = {
                    "status": False,
                    "message": e.args,
                }
                return Response(data, status.HTTP_401_UNAUTHORIZED)
        return Response(serializer_data.errors, status.HTTP_400_BAD_REQUEST)
