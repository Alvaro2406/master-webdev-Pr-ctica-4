from rest_framework.test import APITestCase
import json

from django.urls import reverse
from api_view_roles.models import Role
from viewset_usuarios.models import User


class RoleViewSetAPITests(APITestCase):
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

    def login_as_admin(self):
        login_url = reverse("login")  
        res = self.client.post(
            login_url,
            data={"username": self.username_ok, "password": self.password_ok},
            format="json",
        )
        

    def test_list_roles_successful(self):
        self.login_as_admin()
        list_url = reverse("role-list")
        res = self.client.get(list_url, format="json")
        body = res.json()
        self.assertEqual(len(body), 2)
        self.assertEqual(res.status_code, 200)
    
    def test_create_role_successful(self):
        self.login_as_admin()
        create_url = reverse("role-list")
        payload = {
            "name": "NuevoRol",
            "description": "Descripcion del nuevo rol",
        }
        res = self.client.post(create_url, data=payload, format="json")
        
        body = res.json()
        self.assertEqual(res.status_code, 201)
        self.assertEqual(body["name"], payload["name"])
        self.assertEqual(body["description"], payload["description"])

    def test_update_role_successful(self):
        self.login_as_admin()
        role = Role.objects.create(
            name="RolParaActualizar",
            description="Descripcion inicial",
        )
        update_url = reverse("role-detail", args=[role.id_role])
        payload = {
            "name": "RolActualizado",
            "description": "Descripcion actualizada",
        }
        res = self.client.put(update_url, data=payload, format="json")
        
        body = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(body["name"], payload["name"])
        self.assertEqual(body["description"], payload["description"])

    def test_update_without_permission(self):
        
        role = Role.objects.create(
            name="RolSinPermiso",
            description="Descripcion inicial",
        )
        update_url = reverse("role-detail", args=[role.id_role])
        payload = {
            "name": "IntentoActualizacion",
            "description": "Intento sin permiso",
        }
        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 401)

    def test_delete_role_successful(self):
        self.login_as_admin()
        role = Role.objects.create(
            name="RolParaEliminar",
            description="Descripcion del rol a eliminar",
        )
        delete_url = reverse("role-detail", args=[role.id_role])
        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 204)

    def test_delete_without_permission(self):
        role = Role.objects.create(
            name="RolEliminarSinPermiso",
            description="Descripcion del rol a eliminar sin permiso",
        )
        delete_url = reverse("role-detail", args=[role.id_role])
        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 401)