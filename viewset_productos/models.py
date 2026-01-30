from django.db import models
from api_view_establecimiento.models import Establecimiento

# Create your models here.
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE, related_name='productos')
    

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': str(self.precio),
            'establecimiento_id': self.establecimiento.id_establecimiento
        }
    
    class Meta:
        ordering = ['id_producto']