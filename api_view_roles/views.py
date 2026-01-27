from rest_framework import viewsets
from .models import Role
from .serializer import RoleSerializer
from rest_framework import status
from rest_framework.response import Response

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id_role'