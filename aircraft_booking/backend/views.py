from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets
from backend.serializers import UserSerializer, GroupSerializer, AircraftSerializer
from rest_framework.permissions import IsAuthenticated
from backend.models import Aircraft

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


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

    #Required for authentication
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Aircraft.objects.all()
        aircraft_type = self.request.query_params.get('aircraft_type', None)
        if aircraft_type is not None:
            queryset = queryset.filter(aircraft_type=aircraft_type)
        return queryset



def status(request):
    return JsonResponse({'status': 'OK'})
