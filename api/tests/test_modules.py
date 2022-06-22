from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Module

class Modules(APITestCase):

    def test_create_module(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_overlapping_modules(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        post_data = {
            "teacher": self.user.id,
            "start_time": "12:30:00",
            "end_time": "13:30:00",
            "date": "2023-05-05",
        }

        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:30:00",
            "end_time": "14:30:00",
            "date": "2023-05-05",
        }

        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:30:00",
            "end_time": "13:50:00",
            "date": "2023-05-05",
        }

        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_multiple_valid_modules(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_data = {
            "teacher": self.user.id,
            "start_time": "12:00:00",
            "end_time": "13:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post_data = {
            "teacher": self.user.id,
            "start_time": "14:00:00",
            "end_time": "15:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_module(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.user, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")

        response = self.client.patch(
            f'/api/module/?id={self.module.id}', {"start_time": "13:00:00", "end_time": "14:00:00", "date": "2023-05-07", })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_module(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.user, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")

        response = self.client.delete(
            f'/api/module/?id={self.module.id}', {"start_time": "13:00:00", "end_time": "14:00:00", "reservation_bool": True, "date": "2023-05-07"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_module_as_not_teacher(self):
        self.user = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token))

        post_data = {
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "reservation_bool": False,
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_module_on_past_date(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        post_data = {
            "teacher": self.user.id,
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "date": "2021-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "The date or time you entered is in the past")

    def test_create_module_with_start_after_end(self):

        self.user = get_user_model().objects.create_user(
            mail="user1@uc.cl",
            password="pass1234test..",
            first_name="first_name",
            last_name="last_name",
            phone="66783358",
            is_teacher=True)
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        post_data = {
            "teacher": self.user.id,
            "start_time": "14:00:00",
            "end_time": "13:00:00",
            "date": "2023-05-05",
        }
        response = self.client.post(
            '/api/module/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "The start time must be before the end time")
