from django.test import TestCase, Client
from django.urls import reverse
from ..forms import CustomUserCreationForm
from ..models import AuthUser
import datetime
import json


class TestUsers(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('bank:register')
        self.login_url = reverse('bank:login')
        self.personal_account_url = reverse('bank:personal_account')
        self.users_list_url = reverse('bank:users_list')

        # Создаем тестового пользователя для некоторых тестов
        self.test_user = AuthUser.objects.create(
            username='testuser',
            password='secret123',
            is_superuser=True,
            is_staff=True,
            is_active=True,
            date_joined=datetime.date(2025, 9,9),
            email='test@example.com'
        )

    def test_register_view_success(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'password': 'strongpassw0rd!'
        })
        self.assertEqual(response.status_code, 200)

    def test_register_view_invalid_form(self):
        response = self.client.post(self.register_url, {})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(AuthUser.objects.filter(username='invaliduser').exists())

    def test_login_view_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'is_superuser': '1',
            'password': 'wrong_password'
        })
        self.assertFalse(response.json()['success'])