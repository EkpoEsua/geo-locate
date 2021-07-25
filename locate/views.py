from django.shortcuts import render
from rest_framework import generics, serializers
from locate.models import Provider, ServiceArea
from locate.serializers import ProviderSerializer, ServiceAreaSerializer

# Create your views here.


class ProviderList(generics.ListCreateAPIView):
    """Create view to list all providers, or create a new one"""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ProviderDetail(generics.RetrieveUpdateDestroyAPIView):
    """Create view to give detail, update or delete a provider"""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaList(generics.CreateAPIView):
    """Create view to List or Create a service area for a provider"""
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(provider=Provider.objects.get(pk=self.kwargs['pk']))
    
    def perform_create(self, serializer):
        data = Provider.objects.get(pk=self.kwargs['pk'])
        serializer.save(provider=data)

class ServiceAreaDetail(generics.RetrieveUpdateDestroyAPIView):
    """Create view to give detail, update or delete a Service area"""
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


