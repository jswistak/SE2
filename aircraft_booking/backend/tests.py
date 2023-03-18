from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from .views import UserViewSet, GroupViewSet, AircraftViewSet


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
