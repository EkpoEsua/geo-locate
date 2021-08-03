from django.http import response
from django.urls import reverse
from django.urls.base import resolve
from rest_framework.test import APITestCase
from rest_framework import status
from locate.models import Provider, ServiceArea
from locate.tests.coordinates_n_providers import providers


class ProviderTest(APITestCase):
    def setUp(self):
        url = reverse("provider-list")
        self.data = providers

        self.response_data = []

        for entry in self.data:
            response = self.client.post(url, data=entry, format='json')
            self.response_data.append(response)

    def test_create_provider(self):
        """Ensure proper creation of a provider"""
        response = self.response_data[0]
        data = response.data

        provider = Provider.objects.get(pk=data['id'])
        service_area = ServiceArea.objects.all().filter(provider=provider)
        number_of_servie_areas = len(service_area)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 5)
        self.assertEqual(provider.name, data["name"])
        self.assertEqual(provider.email, data["email"])
        self.assertEqual(provider.phone_number, data["phone_number"])
        self.assertEqual(provider.language, data["language"])
        self.assertEqual(provider.currency, data["currency"])
        self.assertEqual(number_of_servie_areas, 0)

    def test_retrieval_of_providers(self):
        """Test the list of providers returned"""
        url = reverse('provider-list')

        response = self.client.get(url, format='json')
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 5)
        self.assertEqual(data['count'], 5)

    def test_retrieval_of_a_specific_provider(self):
        """Test the retrieval of a specific provider"""
        provider = self.response_data[0].data
        end_point = reverse('provider-detail', args=[provider['id']])

        response = self.client.get(end_point, format='json')
        host = 'http://testserver'

        data = response.data

        self.assertEqual(data['url'], host+end_point)
        self.assertEqual(data['name'], "GIGM")
        self.assertEqual(data['email'], "gigm@gigm.com")

        self.assertEqual(data['phone_number'], "0812345678")
        self.assertEqual(data['language'], "en")
        self.assertEqual(data['currency'], "ngn")

        self.assertEqual(data['currency'], "ngn")
        self.assertEqual(data['service_area_list'],
                         host + reverse('service-area-list', args=[provider['id']]))
        self.assertEqual(len(data['service_areas']), 0)

    def test_update_of_provider(self):
        """Test update of a provider's information"""
        provider = self.response_data[1].data
        provider_url = provider['url']
        
        update_data = {
            "name": "Taxify",
            "email": "taxify@taxify.com",
            "phone_number": "09123456789",
            "language": "fr",
            "currency": "cad"
        }

        response = self.client.patch(provider_url, data=update_data, format='json')
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["name"], update_data["name"])
        self.assertEqual(response_data["email"], update_data["email"])
        self.assertEqual(response_data["phone_number"], update_data["phone_number"])
        self.assertEqual(response_data["language"], update_data["language"])
        self.assertEqual(response_data["currency"], update_data["currency"])

    def test_deletion_of_providers(self):
        """Test Deletion of a provider"""
        provider = self.response_data[2].data
        provider_url = provider['url']

        number_of_providers_before_delete = Provider.objects.count()

        response = self.client.delete(provider_url, format='json')

        number_of_providers_after_delete = Provider.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(number_of_providers_after_delete, number_of_providers_before_delete-1)

        #try getting deleted item
        response = self.client.get(provider_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_creation_of_duplicate_entry_fails(self):
        """Test creation of duplicate provider entry fails"""
        url = reverse('provider-list')

        data = {
            "name": "YSG",
            "email": "ysg@ysg.com",
            "phone_number": "0812345676",
            "language": "fr",
            "currency": "usd"
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_creation_of_service_area_for_a_provider(self):
    #     """
    #     Test provider has created service area
    #     """
