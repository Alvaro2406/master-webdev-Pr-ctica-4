from rest_framework.test import APITestCase
import json
from django.urls import reverse
from api_view_roles.models import Role
from viewset_usuarios.models import User
from api_view_establecimiento.models import Establecimiento
from viewset_productos.models import Producto
from .models import Pedido

class PedidoViewSetAPITests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(
            name="Administrador",
            description="Rol con permisos administrativos",
        )
        self.role_user = Role.objects.create(
            name="Usuario",
            description="Rol de usuario regular",
        )
        self.username_ok = "admin"
        self.password_ok = "123"
        self.user_admin = User.objects.create(
            username=self.username_ok,
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            password=self.password_ok,
            role=self.role_admin,
        )
        self.user_regular = User.objects.create(
            username="user1",
            email="user1@example.com",
            first_name="User",
            last_name="One",
            password="userpass",
            role=self.role_user,
        )

        self.establecimiento = Establecimiento.objects.create(
            nombre="Establecimiento1",
            direccion="Direccion 123",
            telefono="1234567890",
            email="example@business.es",
            id_propietario=self.user_admin,
        )

        self.producto1 = Producto.objects.create(
            nombre="ProductoA",
            descripcion="Descripcion A",
            precio="9.99",
            establecimiento=self.establecimiento,
        )
        self.producto2 = Producto.objects.create(
            nombre="ProductoB",
            descripcion="Descripcion B",
            precio="14.99",
            establecimiento=self.establecimiento,
        )

        self.pedido = Pedido.objects.create(
            usuario=self.user_regular,
            precio_total=24.98,
        )
        self.pedido.productos.set([self.producto1, self.producto2])

    def login_as_admin(self):
        login_url = reverse("login")  
        res = self.client.post(
            login_url,
            data={"username": self.username_ok, "password": self.password_ok},
            format="json",
        )

    def login_as_user(self):
        login_url = reverse("login")  
        res = self.client.post(
            login_url,
            data={"username": "user1", "password": "userpass"},
            format="json",
        )

########################################################################################################################################################################################################
########################################################################################################################################################################################################
    def test_create_order_successful(self):
        self.login_as_user()
        create_url = reverse("pedido_create")
        
        payload = {
            "productos": [self.producto1.id_producto, self.producto2.id_producto],
            "id_usuario": self.user_regular.id_user,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["precio_total"], str(24.98))

    def test_create_order_product_not_found(self):
        self.login_as_user()
        create_url = reverse("pedido_create")
        
        payload = {
            "productos": [999],  
            "id_usuario": self.user_regular.id_user,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 404)

    def test_list_orders_as_admin(self):
        self.login_as_admin()
        list_url = reverse("pedido_list")
        
        res = self.client.get(list_url)
        self.assertEqual(res.status_code, 200)

    def test_update_order_successful(self):
        self.login_as_admin()
        create_url = reverse("pedido_create")
        
        payload = {
            "productos": [self.producto1.id_producto],
            "id_usuario": self.user_regular.id_user,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 201)
        pedido_id = res.json()["id_pedido"]

        update_url = reverse("pedido_update", args=[pedido_id])
        update_payload = {
            "productos": [self.producto1.id_producto, self.producto2.id_producto],
            "id_usuario": self.user_regular.id_user,
        }

        res_update = self.client.put(update_url, data=update_payload, format="json")
        self.assertEqual(res_update.status_code, 200)
        self.assertEqual(res_update.json()["precio_total"], str(24.98))

    def test_delete_order_successful(self):
        self.login_as_user()
        

        delete_url = reverse("pedido_delete", args=[self.pedido.id_pedido])
        res_delete = self.client.delete(delete_url)
        print(res_delete.json())
        self.assertEqual(res_delete.status_code, 200)
        