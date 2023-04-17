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

    def __str__(self):
        return self.user.__str__()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_staff(self):
        return True


class Booking(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    pilot = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pilot')
    instructor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='instructor', null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.aircraft.__str__()} - {self.pilot}, {self.start_time} - {self.end_time}"
