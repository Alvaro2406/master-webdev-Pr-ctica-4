from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'username', 'email', 'first_name', 'last_name', 'password', 'birth_date', 'date_joined', 'points']
        read_only_fields = ['id_user', 'date_joined', 'points']