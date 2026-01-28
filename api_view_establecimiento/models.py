from django.db import models
from viewset_usuarios.models import User

# Create your models here.
class Establecimiento(models.Model):
    id_establecimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    id_propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='establecimientos')

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        return {
            "id_establecimiento": self.id_establecimiento,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "email": self.email,
            "id_propietario": self.id_propietario.id_user
        }