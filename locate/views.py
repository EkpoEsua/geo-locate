from re import L
from django.shortcuts import render
from rest_framework import generics, serializers
from locate.models import Provider, ServiceArea, Coordinate
from locate.serializers import ProviderSerializer, SearchServiceAreasSerializer, \
    ServiceAreaSerializer, CoordinateSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from shapely.geometry import Polygon, Point
from rest_framework.schemas.openapi import AutoSchema

# Create your views here.

class ProviderList(generics.ListCreateAPIView):
    """
    - GET method - List all providers.
    - POST method - Create a new provider.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - GET method - Return details of a specific provider.
    - PATCH or PUT method - Update provider information.
    - DELETE method - Delete a provider.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ServiceAreaList(generics.ListCreateAPIView):
    """
    - GET method - List all the service areas associated with a provider.
    - POST method - Create a service area for the given provider.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        """Return only the service areas belonging to a specific provider identified by it's
        primary key
        """
        return queryset.filter(provider=Provider.objects.get(pk=self.kwargs['pk']))

    def perform_create(self, serializer):
        data = Provider.objects.get(pk=self.kwargs['pk'])
        serializer.save(provider=data)


class ServiceAreaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    - GET method - Return details about a service area.
    - PATCH or PUT method - Modifiy a service area.
    - DELETE method - Remove a service area.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CoordinateList(generics.ListAPIView):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CoordinateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SearchServiceAreas(generics.ListAPIView):
    """
    List all the service areas available at location.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = SearchServiceAreasSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        latitude = self.request.GET['lat']
        longitude = self.request.GET['lon']

        point = Point(float(latitude), float(longitude))

        list_of_service_area_id = []
        for service_area in queryset:
            coordinates = service_area.coordinates.all()
            polygon_points = []
            for coordinate in coordinates:
                polygon_points.append([coordinate.latitude,coordinate.longitude])
            polygon = Polygon(polygon_points)
            if polygon.contains(point):
                list_of_service_area_id.append(service_area.id)

        return queryset.filter(pk__in=list_of_service_area_id)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'][0].pop('coordinates')
        response.data['results'][0].pop('id')
        return response

