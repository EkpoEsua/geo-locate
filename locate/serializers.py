import django
from rest_framework import serializers
from .models import Provider, ServiceArea  # Coordinate


message = "Invalid geojson data"
geojson_error_messages = {
    "incorrect_type": message,
    "incorrect_format": message,
    "not_a_list": message,
    "empty": message,
    "min_length": message,
    "max_length": message,
    "invalid": message,
    "max_value": message,
    "min_value": message,
    "max_string_length": message,
}


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    service_areas = serializers.HyperlinkedRelatedField(
        many=True, view_name="service-area-detail", read_only=True
    )
    service_area_list = serializers.HyperlinkedIdentityField(
        view_name="service-area-list"
    )

    class Meta:
        model = Provider
        fields = [
            "url",
            "id",
            "name",
            "email",
            "phone_number",
            "language",
            "currency",
            "service_area_list",
            "service_areas"
            # "add_service_area"
        ]


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="service-area-detail")
    provider = serializers.StringRelatedField()
    id = serializers.ReadOnlyField()

    class Meta:
        model = ServiceArea
        fields = ["url", "id", "name", "price", "polygon", "provider"]


class SearchServiceAreasSerializer(serializers.ModelSerializer):
    provider = serializers.StringRelatedField()

    class Meta:
        model = ServiceArea
        fields = ["name", "provider", "price"]
