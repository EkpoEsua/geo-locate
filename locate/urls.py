from django.urls import path
from django.views.generic.base import RedirectView
from locate import views

app_name = 'locate'
urlpatterns = [
    # path('', RedirectView(url=())),
    path('providers/', views.ProviderList.as_view(), name='provider-list'),
    path('providers/<int:pk>/', views.ProviderDetail.as_view(), name='provider-detail'),
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
]