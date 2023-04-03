from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from .views import UserViewSet, RegisterView, GroupViewSet, AircraftViewSet, status
import json


class UserTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        User.objects.create_user("jakub", "jakub@email.com", "password")

    def test_user_exists(self):
        request = self.factory.get('/users/')
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_user_has_username(self):
        request = self.factory.get('/users/')
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data[0]['username'], 'jakub')

    def test_user_has_email(self):
        request = self.factory.get('/users/')
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data[0]['email'], 'jakub@email.com')

    def test_user_has_no_password(self):
        request = self.factory.get('/users/')
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertNotIn('password', response.data[0])


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_registration_success(self):
        data = {"username": "justyna",
                "email": "justyna@email.com",
                "password": "password123!23",
                "first_name": "Justyna",
                "last_name": "Pokora"
                }
        request = self.factory.post('/api/register/', data)
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"username": "justyna", "email": "justyna@email.com",
                                         "first_name": "Justyna", "last_name": "Pokora"})

    def test_registration_invalid_email(self):
        data = {"username": "justyna",
                "email": "email",
                "password": "password123!23",
                "first_name": "Justyna",
                "last_name": "Pokora"
                }
        request = self.factory.post('/api/register/', data)
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_registration_invalid_password_too_short(self):
        data = {"username": "justyna",
                "email": "justyna@email.com",
                "password": "123",
                "first_name": "Justyna",
                "last_name": "Pokora"
                }
        request = self.factory.post('/api/register/', data)
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

    def test_registration_invalid_password_common(self):
        data = {"username": "justyna",
                "email": "justyna@email.com",
                "password": "password",
                "first_name": "Justyna",
                "last_name": "Pokora"
                }
        request = self.factory.post('/api/register/', data)
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)

    def test_registration_username_already_exists(self):
        User.objects.create_user("justyna", "justyna@email.com", "password123!23")
        data = {"username": "justyna",
                "email": "justyna2@email.com",
                "password": "password123!23",
                "first_name": "Justyna",
                "last_name": "Pokora"
                }
        request = self.factory.post('/api/register/', data)
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)
        self.assertIn("A user with that username already exists.", str(response.data))

    def test_registration_email_already_exists(self):
        User.objects.create_user("justyna", "justyna@email.com", "password123!23")
        data = {"username": "justyna2",
                "email": "justyna@email.com",
                "password": "password123!23",
                "first_name": "Justyna",
                "last_name": "Pokora"
                }
        request = self.factory.post('/api/register/', data)
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)
        self.assertIn("This field must be unique.", str(response.data))


class StatusTestCase(TestCase):

    def test_status_endpoint(self):
        request = self.client.get('/status/')
        response = status(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"status": "OK"})
