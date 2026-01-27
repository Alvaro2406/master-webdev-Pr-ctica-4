from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id_user'