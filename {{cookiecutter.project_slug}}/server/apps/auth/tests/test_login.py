from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import User


class LoginTest(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.route = "/auth/login/"

        self.email = "test@nomadicode.com"
        self.password = "testpass1234"

        User.objects.create_user(
            first_name="Test",
            last_name="User",
            email=self.email,
            password=self.password
        )


    def test_login_with_correct_credentials(self):
        body = {
            "email": "test@nomadicode.com",
            "password": "testpass1234"
        }

        response = self.api.post(self.route, body)
        self.assertEqual(response.data["status"], "success")

    def test_login_bad_email_good_password(self):
        body = {
            "email": "testbad@nomadicode.com",
            "password": "testpass1234"
        }

        response = self.api.post(self.route, body)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "The email and password combination is incorrect")

    def test_login_good_email_bad_password(self):
        body = {
            "email": "test@nomadicode.com",
            "password": "testpassbad"
        }

        response = self.api.post(self.route, body)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["message"], "The email and password combination is incorrect")
    
    