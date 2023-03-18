from django.db import models


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
