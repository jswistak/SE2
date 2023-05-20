from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group


from .views import UserViewSet, RegisterView, GroupViewSet, AircraftViewSet, status, CertificateViewSet, BookingViewSet
from .models import Staff, Certificate, Aircraft, Booking
from rest_framework.test import APIClient, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
import json
from datetime import datetime


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

    # TODO: just admin can create new aircraft
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

    def test_aircraft_modify(self):
        request_data = {'aircraft_id': 'SP-KOS',
                        'aircraft_name': 'name', 'aircraft_type': "C152", 'aircraft_capacity': 4,
                        'aircraft_range': 1000,
                        'aircraft_speed': 100, 'aircraft_fuel': 100, 'aircraft_status': 'available',
                        'aircraft_cost_per_hour': 1000, 'aircraft_fuel_cost': 10}
        request = self.factory.put('/SP-KOS/', data=request_data, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = AircraftViewSet.as_view({'put': 'update'})(request, pk='SP-KOS')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertEqual(data['aircraft_id'], 'SP-KOS')
        self.assertEqual(data['aircraft_type'], 'C152')


class CertificateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user("user", "user@email.com", "password")
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.certificate = Certificate.objects.create(certificate_name='cert1')

    def test_get_certificates_unauthorized(self):
        request = self.factory.get('/certificate/')
        response = CertificateViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)

    def test_get_certificates_user(self):
        request = self.factory.get('/certificate/')
        force_authenticate(request, user=self.user)
        response = CertificateViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_certificates_admin(self):
        request = self.factory.get('/certificate/')
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_specific_certificate_admin(self):
        request = self.factory.get(f'/certificate/{self.certificate.certificate_name}')
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_certificate_user(self):
        request_data = {'certificate_name': 'cert2'}
        request = self.factory.post('/certificate/', request_data)
        force_authenticate(request, user=self.user)
        response = CertificateViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 403)
        self.assertIn("permission_denied", str(response.data))

    def test_add_certificate_admin(self):
        request_data = {'certificate_name': 'cert2'}
        request = self.factory.post('/certificate/', request_data)
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['certificate_name'], 'cert2')

    def test_add_certificate_already_exists_admin(self):
        request_data = {'certificate_name': self.certificate.certificate_name}
        request = self.factory.post('/certificate/', request_data)
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("certificate with this certificate name already exists", str(response.data))

    def test_modify_certificate_user(self):
        request_data = {'certificate_name': 'certificate1'}
        request = self.factory.put('/certificate/', data=request_data, content_type='application/json')
        force_authenticate(request, user=self.user)
        response = CertificateViewSet.as_view({'put': 'update'})(request, pk='cert1')
        self.assertEqual(response.status_code, 403)
        self.assertIn("permission_denied", str(response.data))

    def test_modify_certificate_admin(self):
        request_data = {'certificate_name': 'certificate1'}
        request = self.factory.put('/certificate/', data=request_data, content_type='application/json')
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'put': 'update'})(request, pk=self.certificate.certificate_name)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content.decode())
        self.assertEqual(response['certificate_name'], 'certificate1')

    def test_modify_certificate_not_found_admin(self):
        request_data = {'certificate_name': 'certificate1'}
        request = self.factory.put('/certificate/', data=request_data, content_type='application/json')
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'put': 'update'})(request, pk='certificate1')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", str(response.data))

    def test_delete_certificate_user(self):
        request = self.factory.delete(f'/certificate/{self.certificate.certificate_name}/')
        force_authenticate(request, user=self.user)
        response = CertificateViewSet.as_view({'delete': 'destroy'})(request, pk=self.certificate.certificate_name)
        self.assertEqual(response.status_code, 403)
        self.assertIn("permission_denied", str(response.data))

    def test_delete_certificate_admin(self):
        request = self.factory.delete(f'/certificate/{self.certificate.certificate_name}/')
        force_authenticate(request, user=self.admin)
        response = CertificateViewSet.as_view({'delete': 'destroy'})(request, pk=self.certificate.certificate_name)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        with self.assertRaises(Certificate.DoesNotExist):
            Certificate.objects.get(certificate_name=self.certificate.certificate_name)


class BookingTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()

        staff_user1 = User.objects.create_user(username='staff_user1', password='password1')
        staff_user2 = User.objects.create_user(username='staff_user2', password='password2')
        certificate = Certificate.objects.create(certificate_name='cert1')
        self.staff1 = Staff.objects.create(user=staff_user1)
        self.staff1.certificates.set([certificate])
        self.staff2 = Staff.objects.create(user=staff_user2)
        self.staff2.certificates.set([certificate])

        self.aircraft1 = Aircraft.objects.create(aircraft_id='SP-KOS', aircraft_name='name1', aircraft_type="C182",
                                                 aircraft_capacity=4, aircraft_range=1000, aircraft_speed=100,
                                                 aircraft_fuel=100, aircraft_cost_per_hour=1000)
        self.aircraft2 = Aircraft.objects.create(aircraft_id='SP-KOG', aircraft_name='name2', aircraft_type="C182",
                                                 aircraft_capacity=4, aircraft_range=1000, aircraft_speed=100,
                                                 aircraft_fuel=100, aircraft_cost_per_hour=1000)

        self.pilot_user1 = User.objects.create_user("user1", "user1@email.com", "password1")
        self.pilot_user2 = User.objects.create_user("user2", "user2@email.com", "password2")

        self.booking1 = Booking.objects.create(aircraft=self.aircraft1, pilot=self.pilot_user1, instructor=self.staff1,
                                               start_time=datetime(2023, 4, 18, 10, 30),
                                               end_time=datetime(2023, 4, 18, 20, 30))
        self.booking2 = Booking.objects.create(aircraft=self.aircraft2, pilot=self.pilot_user2,
                                               start_time=datetime(2023, 4, 20, 10, 30),
                                               end_time=datetime(2023, 4, 20, 20, 30))

    def test_get_bookings_unauthorized(self):
        request = self.factory.get('/booking/')
        response = BookingViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Authentication credentials were not provided", str(response.data))

    def test_get_bookings_pilot(self):
        request = self.factory.get('/booking/')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_bookings_staff(self):
        request = self.factory.get('/booking/')
        force_authenticate(request, user=self.staff1)
        response = BookingViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_bookings_specific_aircraft(self):
        data = {'aircraft': self.aircraft1.pk}
        request = self.factory.get('/booking/', data)
        force_authenticate(request, user=self.staff1)
        response = BookingViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_bookings_specific_pilot(self):
        data = {'pilot': self.pilot_user1.pk}
        request = self.factory.get('/booking/', data)
        force_authenticate(request, user=self.staff1)
        response = BookingViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_bookings_in_time_period(self):
        time_str = '2023-04-19T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-21T10:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'start_time': time1, 'end_time': time2}
        request = self.factory.get('/booking/', data)
        force_authenticate(request, user=self.staff1)
        response = BookingViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_modify_booking_pilot_failed(self):
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft2.pk])}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 400)

    def test_modify_booking_pilot_unauthorized_failed(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft2.pk]),
                'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                'start_time': time1,
                'end_time': time2}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.pilot_user2)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found.", str(response.data))

    def test_modify_booking_pilot_success(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft2.pk]),
                'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                'start_time': time1,
                'end_time': time2}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 200)

    def test_modify_booking_pilot_failed_aircraft_time_taken(self):
        time_str = '2023-04-20T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-20T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft2.pk]),
                'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                'start_time': time1,
                'end_time': time2}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'false', 'message': 'Booking overlap.'})

    def test_modify_booking_staff(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft2.pk]),
                'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                'start_time': time1,
                'end_time': time2}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.staff2)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 200)

    def test_modify_booking_staff_failed_aircraft_time_taken(self):
        time_str = '2023-04-18T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-18T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft1.pk]),
                'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                'start_time': time1,
                'end_time': time2}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'false', 'message': 'Booking overlap.'})

    def test_modify_booking_staff_failed_pilot_time_taken(self):
        time_str = '2023-04-18T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-18T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft2.pk]),
                'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                'start_time': time1,
                'end_time': time2}
        request = self.factory.put('/booking/', data, content_type='application/json')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'false', 'message': 'Booking overlap.'})

    def test_delete_booking_pilot_failed(self):
        request = self.factory.delete(f'/booking/{self.booking2.pk}/')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'delete': 'destroy'})(request, pk=self.booking2.pk)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found.", str(response.data))

    def test_delete_booking_pilot_success(self):
        request = self.factory.delete(f'/booking/{self.booking1.pk}/')
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'delete': 'destroy'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(pk=self.booking1.pk)

    def test_delete_booking_staff(self):
        request = self.factory.delete(f'/booking/{self.booking1.pk}/')
        force_authenticate(request, user=self.staff2)
        response = BookingViewSet.as_view({'delete': 'destroy'})(request, pk=self.booking1.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(pk=self.booking1.pk)

    def test_create_booking_unauthorized(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        request_data = {'aircraft': self.aircraft1.pk, 'pilot': self.pilot_user1.pk, 'instructor': self.staff1.pk,
                'start_time': time1, 'end_time': time2}
        request = self.factory.post('/booking/', request_data)
        response = BookingViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertIn("not_authenticated", str(response.data))

    def test_create_booking_pilot_failed(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        request_data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft1.pk]),
                        'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                        'start_time': time1,
                        'end_time': time2}
        request = self.factory.post('/booking/', request_data)
        force_authenticate(request, user=self.pilot_user2)
        response = BookingViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), {'message': 'Not authenticated.', 'status': 'false'})

    def test_create_booking_pilot_success(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        request_data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft1.pk]),
                        'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                        'start_time': time1,
                        'end_time': time2}
        request = self.factory.post('/booking/', request_data)
        force_authenticate(request, user=self.pilot_user1)
        response = BookingViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    def test_create_booking_staff(self):
        time_str = '2023-04-23T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-23T13:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        request_data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft1.pk]),
                        'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                        'start_time': time1,
                        'end_time': time2}
        request = self.factory.post('/booking/', request_data)
        force_authenticate(request, user=self.staff1)
        response = BookingViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    def test_create_booking_staff_failed_aircraft_time_taken(self):
        time_str = '2023-04-18T10:00:00'
        time1 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        time_str = '2023-04-18T21:00:00'
        time2 = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        request_data = {'aircraft': reverse('aircraft-detail', args=[self.aircraft1.pk]),
                        'pilot': reverse('user-detail', args=[self.pilot_user1.pk]),
                        'start_time': time1,
                        'end_time': time2}
        request = self.factory.post('/booking/', request_data)
        force_authenticate(request, user=self.staff1)
        response = BookingViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {'status': 'false', 'message': 'Booking overlap.'})
