from re import L
from django.shortcuts import render
from rest_framework import generics, serializers
from locate.models import Provider, ServiceArea
from locate.serializers import (
    ProviderSerializer, 
    SearchServiceAreasSerializer,
    ServiceAreaSerializer
)
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError, BadRequest
from rest_framework.schemas.openapi import AutoSchema

# Create your views here.

class ProviderList(generics.ListCreateAPIView):
    """
    - GET method - List all providers.
    - POST method - Create a new provider.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ServiceAreaList(generics.ListCreateAPIView):
    """
    - GET method - List all the service areas associated with a provider.
    - POST method - Create a service area for the given provider.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SearchServiceAreas(generics.ListAPIView):
    """
    List all the service areas available at location.
    """
    queryset = ServiceArea.objects.all()
    serializer_class = SearchServiceAreasSerializer

    def filter_queryset(self, queryset):
        latitude = self.request.GET.get("lat", 0)
        longitude = self.request.GET.get("lon", 0)

        point = Point(float(latitude), float(longitude))

        return queryset.filter(polygon__contains=point)

