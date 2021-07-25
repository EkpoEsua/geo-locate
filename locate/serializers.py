from rest_framework import serializers
from .models import Provider, ServiceArea, Coordinate

class ProviderSerializer(serializers.ModelSerializer):
    service_areas = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceArea.objects.all()
    )
    # service_areas = serializers.HyperlinkedIdentityField(
    #     many=True,
    #     view_name='locsate:service-area-detail',
    #     lookup_field='pk'
    # )
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='locate:provider-detail',
    #     lookup_field='pk'
    # )


    class Meta:
        model = Provider
        fields = [
            'id', 'name',
            'email', 'phone_number', 'language',
            'currency', 'service_areas',
        ]

class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ['latitude', 'longitude', 'service_area']
        read_only_fields = ['service_area']

class ServiceAreaSerializer(serializers.ModelSerializer):
    coordinates = CoordinateSerializer(many=True)
    provider = serializers.ReadOnlyField(source='provider.name')
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='locate:service-area-detail',
    #     lookup_field='pk'
    # )

    class Meta:
        model = ServiceArea
        fields = [
            'name', 'price',
            'coordinates', 'provider'
        ]

    def create(self, validated_data):
        name = validated_data['name']
        price = validated_data['price']
        provider = validated_data['provider']

        print(validated_data)

        service_area = ServiceArea.objects.create(name=name, price=price, provider=provider)

        coordinates = validated_data['coordinates']

        for coordinate in coordinates:
            Coordinate.objects.create(
                latitude=coordinate['latitude'],
                longitude=coordinate['longitude'],
                service_area=service_area
            )
        print()
        print('done!')
        print()

        return service_area
