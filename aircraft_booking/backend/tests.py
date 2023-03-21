from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .views import UserViewSet, GroupViewSet, AircraftViewSet
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenViewBase,
    TokenRefreshView,
    TokenVerifyView,
)

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


class JWTLoginTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user("justyna", "justyna@email.com", "password123")
        self.token = str(RefreshToken.for_user(self.user).access_token)

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

    def test_authenticate_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get('/status/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'OK'})

    def test_authenticate_failure(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + 'invalid_token')
        response = self.client.get('/status/')
        self.assertEqual(response.status_code, 401)
