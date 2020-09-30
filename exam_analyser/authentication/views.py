from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from exam_analyser.authentication.models import User
from exam_analyser.authentication.serializers import UserSerializer


class LoginView(ObtainAuthToken):
    """
    View to get or create the users auth token based on the login credentials given.
    Overridden to include the users profile data along with the response.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context=self.get_renderer_context()
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_data": UserSerializer(
                    user, context=self.get_renderer_context()
                ).data,
            }
        )


class RefreshView(APIView):
    """
    View to refresh or get the currently logged in users data. This cannot be accessed if the users
    token is not present. So the access control enters this view, only if the token is present and valid.
    This just send back the users serializer data.
    """

    def get(self, request, *args, **kwargs):
        return Response(
            UserSerializer(request.user, context=self.get_renderer_context()).data,
        )


class UserViewSet(ModelViewSet):
    """ViewSet to handle the CRUD operations for the users like students and teachers."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
