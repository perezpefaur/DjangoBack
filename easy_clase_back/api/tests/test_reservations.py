from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Module

class Reservations(APITestCase):

    def test_create_reservation(self):
        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_student=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.student, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        post_data = {
            "module": self.module.id
        }
        response = self.client.post(
            '/api/reservation/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_delete_alien_reservation(self):
        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_teacher=True)

        self.student2 = get_user_model().objects.create_user(
            mail="student2@uc.cl",
            password="pass12324test",
            first_name="student2",
            last_name="student2",
            phone="66783358",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.student2, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        post_data = {
            "module": self.module.id
        }
        response = self.client.delete(
            '/api/reservation/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_fail_create_reservations(self):
        self.student = get_user_model().objects.create_user(
            mail="student@uc.cl",
            password="pass1234test",
            first_name="student",
            last_name="student",
            phone="66783359",
            is_teacher=True)

        self.token = RefreshToken.for_user(user=self.student).access_token
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        self.module = Module.objects.create(teacher=self.student, start_time="13:00:00",
                                            end_time="14:00:00", date="2023-05-05")
        post_data = {
            "module": self.module.id
        }
        response = self.client.post(
            '/api/reservation/', post_data, 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
