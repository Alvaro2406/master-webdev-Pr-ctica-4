from rest_framework.test import APITestCase
import json

from django.urls import reverse
from api_view_roles.models import Role
from viewset_usuarios.models import User


class UserViewSetAPITests(APITestCase):
    def setUp(self):
        self.role_prop = Role.objects.create(
            name="Propietario",
            description="Propietario de un establecimiento",
        )
        self.role_admin = Role.objects.create(
            name="Administrador",
            description="Rol con permisos administrativos",
        )

        self.admin_username = "admin1"
        self.admin_password = "adminpass123"
        self.admin_user = User.objects.create(
            username=self.admin_username,
            email="admin1@example.com",
            first_name="Admin",
            last_name="User",
            password=self.admin_password,
            role=self.role_admin,
        )
    def login_as_admin(self):
        login_url = reverse("login")  
        res = self.client.post(
            login_url,
            data={"username": self.admin_username, "password": self.admin_password},
            format="json",
        )
        
    def test_create_user_successful(self):
        self.login_as_admin()
        url = reverse("user-list")  
        create_url = reverse("user-list")

        payload = {
            "username": "user_nuevo",
            "email": "user_nuevo@example.com",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "password": "pass1234",
            "birth_date": "2000-01-01",
            "role": self.role_admin.id_role,
        }

        res = self.client.post(create_url, data=payload, format="json")
        self.assertEqual(res.status_code, 201)

    def test_create_wrong_user(self):
        self.login_as_admin()
        create_url = reverse("user-list")

        payload1 = {
            "username": "",
            "email": "invalidemail",
            "first_name": "Nuevo",
            "last_name": "Usuario",
            "password": "pass1234",
            "birth_date": "2000-01-01",
            "role": self.role_admin.id_role,
        }

        payload2 = {
            "username": "user_nuevo2",
            "email": "user_nuevo2@example.com",
            "first_name": "Nuevo",
            
            "password": "pass1234",
            "birth_date": "2000-01-01",
            "role": self.role_admin.id_role,
        }
        res1 = self.client.post(create_url, data=payload1, format="json")
        res2 = self.client.post(create_url, data=payload2, format="json")
        self.assertEqual(res1.status_code, 400)
        self.assertEqual(res2.status_code, 400)
    
    def test_list_users_successful(self):
        self.login_as_admin()
        list_url = reverse("user-list")

        res = self.client.get(list_url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_list_users_unauthorized(self):
        list_url = reverse("user-list")

        res = self.client.get(list_url, format="json")
        self.assertEqual(res.status_code, 401)

    def test_detail_user_successful(self):
        self.login_as_admin()
        detail_url = reverse("user-detail", args=[self.admin_user.id_user])

        res = self.client.get(detail_url, format="json")
        self.assertEqual(res.status_code, 200)

    def test_detail_user_not_found(self):
        self.login_as_admin()
        detail_url = reverse("user-detail", args=[9999])  

        res = self.client.get(detail_url, format="json")
        self.assertEqual(res.status_code, 404)

    def test_update_user_successful(self):
        self.login_as_admin()
        update_url = reverse("user-detail", args=[self.admin_user.id_user])

        payload = {
            "username": "admin1_updated",
            "email": "admin1_updated@example.com",
            "first_name": "AdminUpdated",
            "last_name": "UserUpdated",
            "password": "newpass123",
            "birth_date": "1990-01-01",
            "role": self.role_admin.id_role,
        }
        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 200)
    
    def test_update_user_not_found(self):
        self.login_as_admin()
        update_url = reverse("user-detail", args=[9999])  

        payload = {
            "username": "nonexistent_user",
            "email": "nonexistent_user@example.com",
            "first_name": "No",
            "last_name": "Exist",
            "password": "nopass",
            "birth_date": "1990-01-01",
            "role": self.role_admin.id_role,
        }
        res = self.client.put(update_url, data=payload, format="json")
        self.assertEqual(res.status_code, 404)

    def test_delete_user_successful(self):
        self.login_as_admin()
        delete_url = reverse("user-detail", args=[self.admin_user.id_user])

        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 204)
    
    def test_delete_user_not_found(self):
        self.login_as_admin()
        delete_url = reverse("user-detail", args=[9999])  

        res = self.client.delete(delete_url, format="json")
        self.assertEqual(res.status_code, 404)
    