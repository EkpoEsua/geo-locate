from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from locate.models import Provider, ServiceArea


class ServiceArea(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_create_service_area(self):
        pass

    def test_retrieval_of_service_area(self):
        pass

    def test_update_service_area(self):
        pass

    def test_deletion_of_service_area(self):
        pass
    