from unittest import result
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from django.http import response
from django.urls import reverse
from django.urls.base import resolve
from django.utils.decorators import decorator_from_middleware
from django.utils.functional import partition
from django.views.decorators.cache import never_cache
from rest_framework.generics import UpdateAPIView
from rest_framework.test import APITestCase
from rest_framework import status
from locate.models import Provider, ServiceArea
from locate.tests.data import providers, provider_x_service_areas


class ServiceAreaTest(APITestCase):
    def setUp(self):
        """setup coordinates, providers, and service areas"""
        url = reverse("provider-list")
        self.data = providers

        self.providers = []

        for entry in self.data:
            response = self.client.post(url, data=entry, format="json")
            self.providers.append(response.data)
        

    def test_creation_of_service_area_for_a_provider(self):
        """Test creation of service areas for a provider"""
        provider = self.providers[0]
        provider_id = provider["id"]
        url = reverse("service-area-list", args=[provider["id"]])

        response = self.client.get(url, format="json")

        service_areas = ServiceArea.objects.filter(provider_id=provider_id)
        data = response.data

        service_area = service_areas.get(pk=2)
        results = data["results"] 
        for result in results:
            if result["id"] == 2:
                returned = result
        
        coordinates = [[]]
        for coordinate in service_area.coordinates.all():
            coordinates[0].append([coordinate.latitude, coordinate.longitude])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 3)
        self.assertEqual(service_areas.count(), 3)
        self.assertEqual(returned["name"], service_area.name)
        self.assertEqual(returned["price"], service_area.price)
        self.assertEqual(returned["provider"], service_area.provider.name)
        self.assertEqual(returned["coordinates"], coordinates)

    # def test_retrieval_of_service_areas_associated_with_a_provider(self):
    #     """Test retrieval of a service areas associated with a provider"""
    #     # get list of providers
    #     url = reverse("provider-list")
    #     response = self.client.get(url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data["count"], 5)
        
    #     # get a specific provider from the response data
    #     provider_url = data["results"][2]["url"]
        
    #     response = self.client.get(provider_url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     #get list of service areas by the provider
    #     list_of_service_area_url = data["service_area_list"]

    #     response = self.client.get(list_of_service_area_url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data["count"], 3)
    #     self.assertEqual(data["next"], None)
    #     self.assertEqual(data["previous"], None)

    #     service_area_names = ["gwarinpa", "jahi", "maitama"]
    #     service_area_ids = [7, 8, 9]
    #     service_area_coordinates = [
    #         maitama_coordinates,
    #         jahi_coordinates,
    #         gwarinpa_coordinates,
    #     ]
    #     service_area_urls = ["http://testserver/service-area/7/",
    #                          "http://testserver/service-area/8/",
    #                          "http://testserver/service-area/9/",]
    #     service_area_price = [800,750,1700,]

    #     for service_area in data["results"]:
    #         service_area = self.client.get(service_area["url"], format="json")
    #         service_area = service_area.data
    #         self.assertIn(service_area["price"], service_area_price)
    #         self.assertIn(service_area["url"], service_area_urls)
    #         self.assertIn(service_area["name"], service_area_names)
    #         self.assertEqual(service_area["provider"], "YSG")
    #         self.assertIn(service_area["id"], service_area_ids)
    #         self.assertIn(service_area["coordinates"], service_area_coordinates)

    # def test_update_service_area(self):
    #     """Test update on a service area associated with provider"""
    #     # get list of providers
    #     url = reverse("provider-list")
    #     response = self.client.get(url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    #     # get a specific provider from the response data
    #     provider_url = data["results"][4]["url"]
        
    #     response = self.client.get(provider_url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     #get list of service areas by the provider
    #     list_of_service_area_url = data["service_area_list"]

    #     response = self.client.get(list_of_service_area_url, format="json")
    #     data = response.data

    #     # get specific service area
    #     service_area_url = data["results"][2]["url"]

    #     update_data = {
    #         "name": "test",
    #         "price": 400,
    #         "coordinates": jahi_coordinates,
    #     }

    #     response = self.client.patch(service_area_url, data=update_data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     response = self.client.get(service_area_url, format="json")
    #     data = response.data

    #     self.assertEqual(data["price"], update_data["price"])
    #     self.assertEqual(data["coordinates"], update_data["coordinates"])
    #     self.assertEqual(data["name"], update_data["name"])

    # def test_deletion_of_service_area(self):
    #     """Test deletion of a service area"""

    #     # get list of providers
    #     url = reverse("provider-list")
    #     response = self.client.get(url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data["count"], 5)
        
    #     # get a specific provider from the response data
    #     provider_url = data["results"][3]["url"]
        
    #     response = self.client.get(provider_url, format="json")
    #     data = response.data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     #get list of service areas by the provider
    #     list_of_service_area_url = data["service_area_list"]

    #     response = self.client.get(list_of_service_area_url, format="json")
    #     data = response.data

    #     # get specific service area
    #     service_area_url = data["results"][2]["url"]
    #     service_area_id = data["results"][2]["id"]

    #     ServiceArea.objects.get(pk=service_area_id)

    #     response = self.client.delete(service_area_url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    #     response = self.client.get(service_area_url, format="json")
    #     self.assertRaises(ServiceArea.DoesNotExist, 
    #                       ServiceArea.objects.get, pk=service_area_id)
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_search_functionality_for_jahi_polygon(self):
        """Test service areas returned for a location search"""
        # Create service areas for each provider using the dictionary mapping
        for key, value in provider_x_service_areas.items():
            p = Provider.objects.get(name=key)
            for service_area in value:
                s, c = ServiceArea.objects.get_or_create(
                    name=service_area.get("name"),
                    defaults={
                        "provider": p,
                        "price": service_area.get("price"),
                        "polygon": str(service_area.get("polygon"))
                    }
                )

        url = reverse("locate")
        point = [
          7.441177368164063,
          9.102774737363891
        ]
        q = f"?lat={point[0]}&lon={point[1]}"
        url = url+q

        response = self.client.get(url, format="json")
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 3)
        
        name_of_service_areas = ["ysg_jahi", "bolt_jahi", "gam_jahi"]
        providers_with_service_areas_in_the_searched_location = [2, 3, 4]
        prices_of_service_areas_in_jahi = [500,750,900]

        for service_area in data["results"]:
            self.assertIn(service_area["name"], name_of_service_areas)
            self.assertIn(service_area["price"], prices_of_service_areas_in_jahi)
            self.assertIn(
                service_area["provider"],
                providers_with_service_areas_in_the_searched_location
            )

    def test_search_functionality_for_a_point_not_in_registered_service_area(self):
        """Test that not results are returned for a point that has not service area available"""
        url = reverse("locate")
        point = [
          7.227630615234374,
          8.879305168312989
        ]
        q = f"?lat={point[0]}&lon={point[1]}"
        url = url+q

        response = self.client.get(url, format="json")
        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"], 0)
        self.assertEqual(data["results"], [])