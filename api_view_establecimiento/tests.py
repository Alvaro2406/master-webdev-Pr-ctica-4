from rest_framework.test import APITestCase
import json

from django.urls import reverse
from api_view_roles.models import Role
from viewset_usuarios.models import User
from .models import Establecimiento

# Create your tests here.
class EstablecimientoViewSetAPITests(APITestCase):
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
            email="example@unex.es",
            id_propietario=self.user_admin,
        )
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
    def test_create_establecimiento_successful(self):
        self.login_as_admin()
        create_url = reverse("establecimiento_create")
        payload = {
            "nombre": "Establecimiento2",
            "direccion": "Direccion 123",
            "telefono": "1234567890",
            "email": "establecimiento2@example.com",
            "id_propietario": self.user_admin.id_user,
        }
        res = self.client.post(create_url, data=payload, format="json")
        
        self.assertEqual(res.status_code, 201)
    
    def test_list_establecimientos_successful(self):
        self.login_as_admin()
        list_url = reverse("establecimiento_list")
        res = self.client.get(list_url, format="json")
        
        self.assertEqual(res.status_code, 200)

        body = res.json()
        self.assertEqual(len(body), 1)

    def test_create_establecimiento_permission_denied(self):
        self.login_as_user()
        create_url = reverse("establecimiento_create")
        payload = {
            "nombre": "Establecimiento2",
            "direccion": "Direccion 123",
            "telefono": "1234567890",
            "email": "establecimiento2@example.com",
            "id_propietario": self.user_admin.id_user,
        }
        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 403)
    
    def test_update_establecimiento_successful(self):
        self.login_as_admin()
        update_url = reverse("establecimiento_update", args=[self.establecimiento.id_establecimiento])
        payload = {
            "nombre": "Establecimiento1 Updated",
            "direccion": "Direccion 456",
            "telefono": "0987654321",
            "email": "establecimiento1updated@example.com",
            "id_propietario": self.user_admin.id_user,
        }
        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 200)

    def test_update_establecimiento_permission_denied(self):
        self.login_as_user()
        
        update_url = reverse("establecimiento_update", args=[self.establecimiento.id_establecimiento])
        payload = {
            "nombre": "Establecimiento1 Updated",
            "direccion": "Direccion 456",
            "telefono": "0987654321",
            "email": "establecimiento1updated@example.com",
            "id_propietario": self.user_admin.id_user,
        }
        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 403)
    
    def test_delete_establecimiento_successful(self):
        self.login_as_admin()
        delete_url = reverse("establecimiento_delete", args=[self.establecimiento.id_establecimiento])
        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_delete_establecimiento_permission_denied(self):
        self.login_as_user()
        delete_url = reverse("establecimiento_delete", args=[self.establecimiento.id_establecimiento])
        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 403)