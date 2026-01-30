from django.db import models
from django.conf import settings
from viewset_usuarios.models import User
from viewset_productos.models import Producto


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")

    productos = models.ManyToManyField(
        Producto,
        related_name="Productos",
    )

    def to_dict(self):
        productos_list = []
        for p in self.productos.all():
            productos_list.append({
                "id_producto": p.id_producto,
                "nombre": p.nombre,
                "precio": str(p.precio),
            })

        return {
            "id_pedido": self.id_pedido,
            "fecha_pedido": self.fecha_pedido.isoformat(),
            "precio_total": str(self.precio_total),
            "id_usuario": self.usuario.id_user,
            "productos": productos_list,
        }
