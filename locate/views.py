from re import L
from django.shortcuts import render
from rest_framework import generics, serializers
from locate.models import Provider, ServiceArea, Coordinate
from locate.serializers import ProviderSerializer, ServiceAreaSerializer, CoordinateSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from shapely.geometry import Polygon, Point


# Create your views here.

class ProviderList(generics.ListCreateAPIView):
    """Create view to list all providers, or create a new one"""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    """Create view to give detail, update or delete a provider"""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ServiceAreaList(generics.ListCreateAPIView):
    """Create view to List or Create a service area for a provider"""
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
    """Create view to give detail, update or delete a Service area"""
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

class Locate(generics.ListAPIView):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @method_decorator(cache_page(60*60*2))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        latitude = self.request.GET['lat']
        longitude = self.request.GET['lon']

        point = Point(float(latitude), float(longitude))

        serializer = self.get_serializer_class()

        serializer = serializer(queryset, many=True, context={'request': self.request})
        list_of_service_area_id = []

        print(type(serializer.data))
        for service_area in serializer.data:
            polygon = Polygon(service_area["coordinates"][0])
            if polygon.contains(point):
                list_of_service_area_id.append(service_area["id"])

        return queryset.filter(pk__in=list_of_service_area_id)