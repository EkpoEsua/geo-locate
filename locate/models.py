from django.contrib.gis.db import models


class Provider(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)

    # Language is encoded in ISO 639-1 format
    language = models.CharField(
        max_length=2, help_text="ISO 639-1 code language format"
    )

    # Currency is encoded in ISO 4217 format
    currency = models.CharField(max_length=3, help_text="ISO 4217 currency format")

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["id"]


class ServiceArea(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    provider = models.ForeignKey(
        "Provider", related_name="service_areas", on_delete=models.CASCADE
    )
    polygon = models.PolygonField(spatial_index=True)

    class Meta:
        ordering = ["id"]
