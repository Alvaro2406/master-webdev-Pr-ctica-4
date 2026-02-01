from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from api_view_login.authentication import CookieJWTAuthentication
from utils.user_validation import HasJWTUser
from .permission import CanListUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id_user'
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [HasJWTUser, CanListUser]
