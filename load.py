import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geo_locate.settings')
django.setup()

from locate.models import Provider, ServiceArea
from locate.tests import data

# Load Provider data
for provider in data.providers:
    p, c = Provider.objects.get_or_create(
        name = provider.get("name"),
        defaults={
            "email": provider.get("email"),
            "phone_number": provider.get("phone_number"),
            "language": provider.get("language"),
            "currency": provider.get("currency")
        }
    )


# Load Service Area data
for key, value in data.provider_x_service_areas.items():
    p = Provider.objects.get(name=key)
    for service_area in value:
        s, c = ServiceArea.objects.get_or_create(
            name=service_area.get("name"),
            defaults={
                "provider": p,
                "price": service_area.get("price"),
                "polygon": str(service_area.get("polygon"))
            }
        )

