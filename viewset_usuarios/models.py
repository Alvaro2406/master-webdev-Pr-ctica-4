from django.db import models
from api_view_roles.models import Role

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['id_user']