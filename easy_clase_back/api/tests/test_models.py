import json
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import RegisterSerializer, UserSerializer
from api.models import UserProfile, Module
from unittest import skip


class Registration(APITestCase):

    def test_registration(self):
        data = {
            "first_name": "testFirst",
            "last_name": "testLast",
            "mail": "test@mail.com",
            "phone": "77483362",
            "comunas": "Lo Barnechea, Santiago, Yangquihue",
            "subjects": "fracciones, sumatorias, calculo",
            "institutions": "craighouse, puc, catolica",
            "price": 10000,
            "description": "Me gustan mucho las matematicas",
            "is_teacher": True,
            "password": "pass123..",
            "password2": "pass123.."
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_mail_successful(self):
        mail = 'test@uc.cl'
        password = 'test'
        first_name = 'test'
        last_name = 'testlast'
        phone = '00000000'
        user = get_user_model().objects.create_user(
            mail=mail,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        self.assertEqual(user.mail, mail)
        self.assertTrue(user.check_password(password))

    def test_new_user_mail_normalized(self):
        mail = 'test@UC.cl'
        password = 'test'
        first_name = 'test'
        last_name = 'testlast'
        phone = '00000000'
        user = get_user_model().objects.create_user(
            mail=mail,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )

        self.assertEqual(user.mail, mail.lower())

    def test_new_user_invalid_mail(self):
        mail = None
        password = 'test'
        first_name = 'test'
        last_name = 'testlast'
        phone = '00000000'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                mail=mail,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )

    def test_create_new_superuser(self):
        mail = 'test1@uc.cl'
        password = 'hola'
        first_name = 'test'
        last_name = 'testlast'
        phone = '00000000'
        user = get_user_model().objects.create_superuser(
            first_name=first_name,
            last_name=last_name,
            mail=mail,
            phone=phone,
            password=password
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class PrivateProfileView(APITestCase):

    profile_url = reverse('get_profile')

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            mail="mail@uc.cl",
            password="pass123..",
            first_name="first_name",
            last_name="last_name",
            phone="66783359"
        )
        self.token = RefreshToken.for_user(user=self.user).access_token
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_profile_authenticated(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PublicProfileView(APITestCase):

    list_teachers_url = reverse('teachers_view')
    profile_teacher_url = reverse('get_teacher', kwargs={"pk": 1})

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            mail="mail@uc.cl",
            password="pass123..",
            first_name="first_name",
            last_name="last_name",
            phone="66783359",
            is_teacher=True
        )

    def test_profile_authenticated(self):
        response = self.client.get(self.list_teachers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_un_authenticated(self):
        response = self.client.get(self.profile_teacher_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
            "teacher": self.user.id,
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


class Reservation(APITestCase):

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
