from django.urls import path
from django.urls.base import reverse_lazy
from django.views.generic.base import RedirectView, TemplateView
from locate import views
from rest_framework.schemas import get_schema_view

# app_name = 'locate'
description = """
An API service for transport service providers and customers.

Transport service providers are identified as "Providers" having the following information:
- Name
- Email
- Phone Number (11-digit)
- Language (Language is encoded in ISO 639-1 format)
- Currency (Currency is encoded in ISO 4217 format)


Once a provider is Created, Service areas can then be defined for the provider.
A provider can be created, updated, and deleted.

A service area is defined by:
- A geojson polygon
- Name
- Price

A service area can be updated and deleted as well.

A customer can make a search to get a list of service areas for a given location.
This location is identified by a lat/lon pair.

The result of a search consists of:
- Service area name
- Price
- Provider name

"""

urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name='locate/swagger-ui.html',
            extra_context={'schema_url':'schema'}
        ), 
        name='swagger-ui'
    ),
    path(
        'schema/',
        get_schema_view(
             title='Geo Locate',
             description=description,
             version='1.0.0'
        ),
        name='schema'
    ),
    path(
        'providers/',
        views.ProviderList.as_view(),
        name='provider-list'
    ),
    path(
        'providers/<int:pk>/',
        views.ProviderDetail.as_view(),
        name='provider-detail'
    ),
    path(
        'providers/<int:pk>/service-area/',
        views.ServiceAreaList.as_view(),
        name='service-area-list'
    ),
    path(
        'service-area/<int:pk>/',
        views.ServiceAreaDetail.as_view(),
        name='service-area-detail'
    ),

    path(
        'search/',
        views.SearchServiceAreas.as_view(),
        name='locate'
    ),
]
