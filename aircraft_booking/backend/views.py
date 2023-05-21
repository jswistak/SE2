from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, generics
from backend.serializers import UserSerializer, GroupSerializer, RegisterSerializer, AircraftSerializer, \
    CertificateSerializer, BookingSerializer, StaffSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from backend.models import Aircraft, Certificate, Booking, Staff


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


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy' :
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

      
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
                Q(start_time__lte=end_time) & Q(end_time__gte=start_time)
            )
        elif start_time:
            queryset = queryset.filter(start_time__gte=start_time)
        elif end_time:
            queryset = queryset.filter(end_time__lte=end_time)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.request.user.is_staff:
            if serializer.validated_data['pilot'] != self.request.user:
                return JsonResponse(status=401, data={'status': 'false', 'message': 'Not authenticated.'})

        queryset = Booking.objects.all()

        try:
            start_time = serializer.validated_data['start_time']
        except KeyError:
            start_time = None
        try:
            end_time = serializer.validated_data['end_time']
        except KeyError:
            end_time = None
        if start_time and end_time:
            queryset = queryset.filter(
                Q(start_time__lte=end_time) & Q(end_time__gte=start_time)
            )
        elif start_time:
            queryset = queryset.filter(start_time__gte=start_time)
        elif end_time:
            queryset = queryset.filter(end_time__lte=end_time)

        try:
            aircraft = serializer.validated_data['aircraft']
        except KeyError:
            aircraft = None
        queryset_aircraft = None
        if aircraft is not None:
            queryset_aircraft = queryset.filter(aircraft=aircraft)

        try:
            pilot = serializer.validated_data['pilot']
        except KeyError:
            pilot = None
        queryset_pilot = None
        if pilot is not None:
            queryset_pilot = queryset.filter(pilot=pilot)

        try:
            instructor = serializer.validated_data['instructor']
        except KeyError:
            instructor = None
        queryset_instructor = None
        if instructor is not None:
            queryset_instructor = queryset.filter(instructor=instructor)

        if queryset_aircraft or queryset_pilot or queryset_instructor:
            return JsonResponse(status=400, data={'status': 'false', 'message': 'Booking overlap.'})

        self.perform_create(serializer)
        return JsonResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        queryset = Booking.objects.all()

        try:
            start_time = serializer.validated_data['start_time']
        except KeyError:
            start_time = None
        try:
            end_time = serializer.validated_data['end_time']
        except KeyError:
            end_time = None
        if start_time and end_time:
            queryset = queryset.filter(
                Q(start_time__lte=end_time) & Q(end_time__gte=start_time)
            )
        elif start_time:
            queryset = queryset.filter(start_time__gte=start_time)
        elif end_time:
            queryset = queryset.filter(end_time__lte=end_time)

        try:
            aircraft = serializer.validated_data['aircraft']
        except KeyError:
            aircraft = None
        queryset_aircraft = None
        if aircraft is not None:
            queryset_aircraft = queryset.filter(aircraft=aircraft)

        try:
            pilot = serializer.validated_data['pilot']
        except KeyError:
            pilot = None
        queryset_pilot = None
        if pilot is not None:
            queryset_pilot = queryset.filter(pilot=pilot)

        try:
            instructor = serializer.validated_data['instructor']
        except KeyError:
            instructor = None
        queryset_instructor = None
        if instructor is not None:
            queryset_instructor = queryset.filter(instructor=instructor)

        if queryset_aircraft or queryset_pilot or queryset_instructor:
            return JsonResponse(status=400, data={'status': 'false', 'message': 'Booking overlap.'})

        self.perform_update(serializer)
        return JsonResponse(serializer.data)
      

def status(request):
    return JsonResponse({'status': 'OK'})
