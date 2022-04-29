import json
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import RegisterSerializer, UserSerializer
from api.models import UserProfile


class Registration(APITestCase):

    def test_registration(self):
        data = {
            "first_name": "testFirst",
            "last_name": "testLast",
            "mail": "test@mail.com",
            "phone": "77483362",
            "comunas": "Lo Barnechea, Santiago, Yangquihue",
            "assignature": "Matematicas, Humanidades",
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
        password = 'test'
        first_name = 'test'
        last_name = 'testlast'
        phone = '00000000'
        user = get_user_model().objects.create_superuser(
            mail=mail,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
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
