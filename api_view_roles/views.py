from rest_framework import viewsets
from .models import Role
from .serializer import RoleSerializer
from api_view_login.authentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.user_validation import HasJWTUser
from .permission import CanUseRoles

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id_role'
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [HasJWTUser, CanUseRoles]