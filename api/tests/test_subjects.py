from rest_framework.test import APITestCase
from rest_framework import status


class Subjects(APITestCase):

    def test_create_subject(self):
        post_data = {
            "name": "Python",
        }
        response = self.client.post(
            '/api/subject/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_subjects_with_filter(self):
        post_data = {
            "name": "Python",
        }
        self.client.post(
            '/api/subject/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        post_data = {
            "name": "Programación",
        }
        self.client.post(
            '/api/subject/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.get('/api/subjects/?name=Python')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'Python')
