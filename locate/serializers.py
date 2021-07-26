from collections import OrderedDict
from django.core.checks import messages
from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from .models import Provider, ServiceArea, Coordinate

message = 'Invalid geojson data'
geojson_error_messages =  {
    'incorrect_type': message,
    'incorrect_format': message,
    'not_a_list': message,
    'empty': message,
    'min_length': message,
    'max_length': message,
    'invalid': message,
    'max_value': message,
    'min_value': message,
    'max_string_length': message
}

value = serializers.FloatField()
coordinate = serializers.ListField(value, min_length=2, max_length=2)

class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    service_areas = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='service-area-detail',
        read_only=True
    )

    service_area_list = serializers.HyperlinkedIdentityField(
        view_name='service-area-list'
    )

    class Meta:
        model = Provider
        fields = [
            'url', 'id', 'name',
            'email', 'phone_number', 'language',
            'currency', 'service_area_list', 'service_areas'
        ]

class CoordinateSerializer(serializers.HyperlinkedModelSerializer):
    service_area = serializers.ReadOnlyField(source='service_area.name')

    class Meta:
        model = Coordinate
        fields = ['url', 'id', 'latitude', 'longitude', 'service_area']


class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    coordinates = serializers.ListField(
            child=serializers.ListField(
                child=serializers.ListField(
                    child=serializers.FloatField(error_messages=geojson_error_messages),
                    min_length=2,
                    max_length=2,
                    error_messages=geojson_error_messages
                ),
                min_length=3,
                error_messages=geojson_error_messages
            ),
            min_length=1,
            max_length=1,
            error_messages=geojson_error_messages
    )
    # coordinates = CoordinateSerializer(many=True, read_only=True)
    provider = serializers.ReadOnlyField(source='provider.name')
    url = serializers.HyperlinkedIdentityField(
        view_name='service-area-detail'
    )

    class Meta:
        model = ServiceArea
        fields = [
            'url', 'id', 'name',
            'price', 'provider', 'coordinates',
        ]

    def create(self, validated_data):
        """save a Service area instance, as well as related coordinate instances as well"""

        # print(validated_data)
        coordinates = validated_data.pop('coordinates')

        # print(coordinates)
        # assert(False)

        service_area = super(ServiceAreaSerializer, self).create(validated_data)

        for coordinate in coordinates[0]:
            Coordinate.objects.create(
                latitude=coordinate[0],
                longitude=coordinate[1],
                service_area=service_area
            )

        # coordinate_serializer = CoordinateSerializer(data=coordinates, many=True)
        # coordinate_serializer.is_valid(raise_exception=True)
        # coordinate_serializer.save(service_area=service_area)

        return service_area

    def update(self, instance, validated_data):
        """update service area instance as well as related coordinate instances as well"""
        coordinates_data = validated_data.pop('coordinates')

        service_area = super(ServiceAreaSerializer, self).update(instance, validated_data)

        service_area.coordinates.all().delete()

        for coordinate in coordinates_data[0]:
            Coordinate.objects.create(
                latitude=coordinate[0],
                longitude=coordinate[1],
                service_area=service_area
            )

        # assert(False)

        return service_area


    def to_representation(self, instance):
        # assert(False)
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue


            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                if field.field_name == 'coordinates':
                    ret[field.field_name] = [[]]
                    continue
                ret[field.field_name] = field.to_representation(attribute)

        coordinate_field = CoordinateSerializer(
            many=True,
            read_only=True,
            context={'request': self.context['request']}
        )

        coordinates = coordinate_field.to_representation(instance.coordinates)
        for coordinate in coordinates:
            ret['coordinates'][0].append([coordinate['latitude'],coordinate['longitude']])
        
        return ret

    