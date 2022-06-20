from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

class Institutions(APITestCase):

    def test_create_institution(self):
        post_data = {
            "name": "PUC",
        }
        response = self.client.post(
            '/api/institution/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_institutions_with_filter(self):
        post_data = {
            "name": "PUC",
        }
        self.client.post(
            '/api/institution/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        post_data = {
            "name": "FEN",
        }
        self.client.post(
            '/api/institution/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.get('/api/institutions/?name=PUC')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'PUC')


