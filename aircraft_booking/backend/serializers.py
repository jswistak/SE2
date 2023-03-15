from django.contrib.auth.models import User, Group
from rest_framework import serializers
from backend.models import Aircraft


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['aircraft_id', 'aircraft_name', 'aircraft_type', 'aircraft_capacity', 'aircraft_range', 'aircraft_speed', 'aircraft_cost_per_hour', 'aircraft_fuel']
