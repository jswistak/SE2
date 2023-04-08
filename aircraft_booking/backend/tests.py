from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User

from .models import Aircraft
from .views import UserViewSet, RegisterView, GroupViewSet, AircraftViewSet, status
from rest_framework.test import APIClient, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
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


class JWTTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user("justyna", "justyna@email.com", "password123")
        self.access_token = str(AccessToken.for_user(self.user))
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_login_success(self):
        request_data = {'username': 'justyna', 'password': 'password123'}
        request = self.factory.post('/api/login/', request_data)
        response = TokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure(self):
        request_data = {'username': 'justyna', 'password': 'wrong_pass'}
        request = self.factory.post('/api/login/', request_data)
        response = TokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_refresh_token_success(self):
        refresh_data = {'refresh': self.refresh_token}
        request = self.factory.post('/api/token/refresh/', refresh_data)
        response = TokenRefreshView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_refresh_token_failure(self):
        refresh_data = {'refresh': 'invalid_token'}
        request = self.factory.post('/api/token/refresh/', refresh_data)
        response = TokenRefreshView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_verify_refresh_token_success(self):
        verify_data = {'token': self.refresh_token}
        request = self.factory.post('/api/token/verify/', verify_data)
        response = TokenVerifyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_verify_access_token_success(self):
        verify_data = {'token': self.access_token}
        request = self.factory.post('/api/token/verify/', verify_data)
        response = TokenVerifyView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_verify_token_failure(self):
        verify_data = {'token': 'invalid_token'}
        request = self.factory.post('/api/token/verify/', verify_data)
        response = TokenVerifyView.as_view()(request)
        self.assertEqual(response.status_code, 401)

class AircraftTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user("user", "user@email.com", "password")
        self.access_token = str(AccessToken.for_user(self.user))
        Aircraft.objects.create(aircraft_id='SP-KOS', aircraft_name='name', aircraft_type="C182", aircraft_capacity=4, aircraft_range=1000, aircraft_speed=100, aircraft_fuel=100, aircraft_cost_per_hour=1000)

    def test_aircraft_list_unauthorized(self):
        request = self.factory.get('/aircraft/')
        response = AircraftViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)
    def test_aircraft_create(self):
        request_data = {'aircraft_id': 'SP-KOG',
                'aircraft_name': 'name', 'aircraft_type': "C182", 'aircraft_capacity': 4, 'aircraft_range': 1000,
                'aircraft_speed': 100, 'aircraft_fuel': 100, 'aircraft_status': 'available',
                'aircraft_cost_per_hour': 1000, 'aircraft_fuel_cost': 10}
        request = self.factory.post('/aircraft/', request_data)
        force_authenticate(request, user=self.user)
        response = AircraftViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['aircraft_id'], 'SP-KOG')

    def test_aircraft_create_unauthorized(self):
        request_data = {'aircraft_id': 'SP-SOP',
                        'aircraft_name': 'name', 'aircraft_type': "C182", 'aircraft_capacity': 4,
                        'aircraft_range': 1000,
                        'aircraft_speed': 100, 'aircraft_fuel': 100, 'aircraft_status': 'available',
                        'aircraft_cost_per_hour': 1000, 'aircraft_fuel_cost': 10}
        request = self.factory.post('/aircraft/', request_data)
        response = AircraftViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)

    def test_aircraft_list(self):
        request = self.factory.get('/aircraft/')
        force_authenticate(request, user=self.user)
        response = AircraftViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_aircraft_detail(self):
        request = self.factory.get('/aircraft/SP-KOS/')
        force_authenticate(request, user=self.user)
        response = AircraftViewSet.as_view({'get': 'retrieve'})(request, pk='SP-KOS')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['aircraft_id'], 'SP-KOS')
