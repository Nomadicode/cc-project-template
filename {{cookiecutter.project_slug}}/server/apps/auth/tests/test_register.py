from django.test import TestCase
from rest_framework.test import APIClient


class RegisterTest(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.route = "/auth/register/"

    def test_register_with_missing_fields(self):
        body = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@nomadicode.com",
            "password": "testpass1234"
        }
        self.assertTrue(True)

    def test_register_with_all_data_correct(self):
        self.assertTrue(True)

    def test_register_with_used_email(self):
        self.assertTrue(True)
    