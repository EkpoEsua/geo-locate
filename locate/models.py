from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case

# Create your models here.


class Provider(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=11, unique=True)

    #Language is encoded in ISO 639-1 format
    language = models.CharField(max_length=2, help_text="ISO 639-1 code language format")

    #Currency is encoded in ISO 4217 format
    currency = models.CharField(max_length=3, help_text="ISO 4217 currency format")


class ServiceArea(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    provider = models.ForeignKey('Provider', related_name='service_areas',
                                on_delete=models.CASCADE)


class Coordinate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    service_area = models.ForeignKey('ServiceArea', related_name='coordinates', on_delete=models.CASCADE)


"""{
    "name": "gwarinpa",
    "price": 1200,
    "coordinate_set": [{"latitude": 30.0, "longitude": 10.0}, {"latitude": 40.0, "longitude": 40.0}, {"latitude": 20.0, "longitude": 40.0}, {"latitude": 10.0, "longitude": 20.0}, {"latitude": 30.0, "longitude": 10.0}]
}"""