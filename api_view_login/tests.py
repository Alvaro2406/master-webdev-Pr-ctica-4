from rest_framework.test import APITestCase
import json

from django.urls import reverse
from api_view_roles.models import Role
from viewset_usuarios.models import User

# Create your tests here.
class LoginViewAPITests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(
            name="Administrador",
            description="Rol con permisos administrativos",
        )
        self.username_ok = "admin"
        self.password_ok = "123"
        self.user_admin = User.objects.create(
            username=self.username_ok,
            email="admin1@example.com",
            first_name="Admin",
            last_name="User",
            password=self.password_ok,
            role=self.role_admin,
        )

    def test_login_ok_returns_tokens_and_sets_cookie(self):
        url = reverse("login")  

        payload = {"username": self.username_ok, "password": self.password_ok}
        res = self.client.post(url, data=payload, format="json")

        self.assertEqual(res.status_code, 200)

        body = res.json()
        self.assertIn("access", body)
        self.assertIn("refresh", body)
        self.assertIn("user_id", body)

    def test_login_wrong_user_returns_401(self):
        url = reverse("login")
        data = {"username": "no_existe", "password": "da_igual"}
        res = self.client.post(url, data=data, format="json")

        self.assertEqual(res.status_code, 401)
        

    def test_login_wrong_password_returns_401(self):
        url = reverse("login")

        data = {"username": self.username_ok, "password": "mal_password"}
        res = self.client.post(url, data=data, format="json")

        self.assertEqual(res.status_code, 401)

    def test_login_invalid_json_returns_400(self):
        url = reverse("login")

        res = self.client.post(
            url,
            data="{ejemplo",
            content_type="application/json",
        )

        self.assertEqual(res.status_code, 400)
        

    def test_login_missing_fields_returns_400(self):
        url = reverse("login")

        res = self.client.post(url, data={"username": self.username_ok}, format="json")

        self.assertEqual(res.status_code, 400)