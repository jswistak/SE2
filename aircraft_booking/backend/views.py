from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import JsonResponse
from requests import Response
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from backend.serializers import UserSerializer, GroupSerializer, AircraftSerializer, RegisterSerializer, \
    BookingSerializer, StaffSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from backend.models import Aircraft, Booking, Staff


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # ermission_classes = [permissions.IsAuthenticated]


class AircraftViewSet(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return JsonResponse(serializer.data)

    # Required for authentication
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Aircraft.objects.all()
        aircraft_type = self.request.query_params.get('aircraft_type', None)
        if aircraft_type is not None:
            queryset = queryset.filter(aircraft_type=aircraft_type)
        return queryset


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = StaffSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    def get_queryset(self):
        queryset = Booking.objects.all()
        if self.request.user.is_staff:
            pass
        elif self.request.user.is_authenticated:
            queryset = queryset.filter(pilot=self.request.user)
        else:
            queryset = queryset.filter(pilot=None)

        aircraft = self.request.query_params.get('aircraft', None)
        if aircraft is not None:
            queryset = queryset.filter(aircraft=aircraft)
        pilot = self.request.query_params.get('pilot', None)
        if pilot is not None:
            queryset = queryset.filter(pilot=pilot)
        instructor = self.request.query_params.get('instructor', None)
        if instructor is not None:
            queryset = queryset.filter(instructor=instructor)
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)
        if start_time and end_time:
            queryset = queryset.filter(
                Q(start_time__gte=start_time) & Q(end_time__lte=end_time)
            )
        elif start_time:
            queryset = queryset.filter(start_time__gte=start_time)
        elif end_time:
            queryset = queryset.filter(end_time__lte=end_time)
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)



def status(request):
    return JsonResponse({'status': 'OK'})
