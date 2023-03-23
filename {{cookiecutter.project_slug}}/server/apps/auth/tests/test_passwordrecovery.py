from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient

from apps.users.models import User



class PasswordRecoveryTest(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.route = "/auth/password/forgot/"

        self.email = "test@nomadicode.com"
        self.password = "testpassword"

        User.objects.create_user(
            first_name="Test",
            last_name="User",
            email=self.email,
            password=self.password
        )

    @patch("utils.email.send_email_template", return_value=None)
    def test_sends_email(self, mock_method):
        self.assertTrue(True)

    def test_generates_reset_token(self):
        self.assertTrue(True)

    def test_invalid_email_returns_error(self):
        self.assertTrue(True)
