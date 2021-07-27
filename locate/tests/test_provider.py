from django.http import response
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from locate.models import Provider, ServiceArea


class ProviderTest(APITestCase):
    def setUp(self):
        url = reverse("provider-list")
        self.data = [
            {
                "name": "GIGM",
                "email": "gigm@gigm.com",
                "phone_number": "0812345678",
                "language": "en",
                "currency": "ngn"
            },
            {
                "name": "Bolt",
                "email": "bolt@bolt.ng",
                "phone_number": "0812345677",
                "language": "en",
                "currency": "ngn"
            },
            {
                "name": "YSG",
                "email": "ysg@ysg.com",
                "phone_number": "0812345676",
                "language": "fr",
                "currency": "usd"
            },
            {
                "name": "GAM",
                "email": "gam@gam.com",
                "phone_number": "0812345675",
                "language": "es",
                "currency": "aud"
            },
            {
                "name": "ABC",
                "email": "abc@abc.com",
                "phone_number": "0812345674",
                "language": "en",
                "currency": "eur"
            },
        ]

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
        pass

    def test_deletion_of_providers(self):
        pass

    def test_creation_of_duplicate_entry_fails(self):
        pass
