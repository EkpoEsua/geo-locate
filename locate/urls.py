from django.urls import path
from django.urls.base import reverse_lazy
from django.views.generic.base import RedirectView
from locate import views

# app_name = 'locate'
urlpatterns = [
    path(
        '',
        RedirectView.as_view(url=reverse_lazy('provider-list')),
        name='home'
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
        'coordinates/', 
         views.CoordinateList.as_view(),
         name='coordinate-list'
    ),
    path(
        'coordinates/<int:pk>', 
         views.CoordinateDetail.as_view(),
         name='coordinate-detail'
    ),
    path(
        'locate/', 
         views.Locate.as_view(),
         name='locate'
    ),
]