from rest_framework.test import APITestCase
import json

from django.urls import reverse
from api_view_roles.models import Role
from viewset_usuarios.models import User
from viewset_productos.models import Producto
from api_view_establecimiento.models import Establecimiento

# Create your tests here.
class ProductoViewSetAPITests(APITestCase):
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

        Producto.objects.create(
            nombre="ProductoA",
            descripcion="Descripcion A",
            precio="9.99",
            establecimiento=self.establecimiento,
        )
        Producto.objects.create(
            nombre="ProductoB",
            descripcion="Descripcion B",
            precio="14.99",
            establecimiento=self.establecimiento,
        )

########################################################################################################################################################################################################
########################################################################################################################################################################################################

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

    def test_create_producto_successful(self):
        self.login_as_admin()
        create_url = reverse("productos-list")

        payload = {
            "nombre": "Producto1",
            "descripcion": "Descripcion del producto 1",
            "precio": "19.99",
            "establecimiento": self.establecimiento.id_establecimiento,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 201)
    def test_create_producto_missing_field(self):
        self.login_as_admin()
        create_url = reverse("productos-list")

        payload = {
            "nombre": "Producto2",
            "descripcion": "Descripcion del producto 2",
            "establecimiento": self.establecimiento.id_establecimiento,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_create_producto_without_permission(self):
        self.login_as_user()
        create_url = reverse("productos-list")

        payload = {
            "nombre": "Producto3",
            "descripcion": "Descripcion del producto 3",
            "precio": "29.99",
            "establecimiento": self.establecimiento.id_establecimiento,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 403)

    def test_list_productos_successful(self):
        self.login_as_admin()
        list_url = reverse("productos-list")
        res = self.client.get(list_url, format="json")
        

        body = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(body), 2)
    
    def test_list_productos_without_authentication(self):
        self.login_as_user()
        list_url = reverse("productos-list")
        res = self.client.get(list_url, format="json")
        self.assertEqual(res.status_code, 403)

    def test_update_producto_successful(self):
        self.login_as_admin()
        producto = Producto.objects.first()
        update_url = reverse("productos-detail", args=[producto.id_producto])

        payload = {
            "nombre": "ProductoA_Updated",
            "descripcion": "Descripcion A Updated",
            "precio": "11.99",
            "establecimiento": self.establecimiento.id_establecimiento,
        }

        res = self.client.put(update_url, data=payload, format="json")
        
        producto.refresh_from_db()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(producto.nombre, "ProductoA_Updated")

    def test_update_producto_not_found(self):
        self.login_as_admin()
        update_url = reverse("productos-detail", args=[9999])  

        payload = {
            "nombre": "NonExistentProduct",
            "descripcion": "No description",
            "precio": "0.00",
            "establecimiento": self.establecimiento.id_establecimiento,
        }

        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 404)

    def test_update_producto_without_permission(self):
        self.login_as_user()
        producto = Producto.objects.first()
        update_url = reverse("productos-detail", args=[producto.id_producto])

        payload = {
            "nombre": "ProductoA_UpdatedByUser",
            "descripcion": "Descripcion A Updated By User",
            "precio": "12.99",
            "establecimiento": self.establecimiento.id_establecimiento,
        }

        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 403)

    def test_delete_producto_successful(self):
        self.login_as_admin()
        producto = Producto.objects.first()
        delete_url = reverse("productos-detail", args=[producto.id_producto])

        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 204)

    def test_delete_producto_not_found(self):
        self.login_as_admin()
        delete_url = reverse("productos-detail", args=[9999])  

        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 404)