from django.db import models
from django.contrib.auth.models import User

class Aircraft(models.Model):
    aircraft_id = models.CharField(max_length=10, primary_key=True)
    aircraft_name = models.CharField(max_length=50)
    aircraft_type = models.CharField(max_length=50)
    aircraft_capacity = models.IntegerField()
    aircraft_range = models.IntegerField()
    aircraft_speed = models.IntegerField()
    aircraft_cost_per_hour = models.IntegerField()
    aircraft_fuel = models.IntegerField()

    def __str__(self):
        return self.aircraft_id

class Certificate(models.Model):
    certificate_name = models.CharField(max_length=50, primary_key=True)
    def __str__(self):
        return self.certificate_name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certificates = models.ManyToManyField(Certificate)

class Booking(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='pilot')
    instructor = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='instructor', null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
