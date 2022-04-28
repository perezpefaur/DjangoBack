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
            "nombre": "testFirst",
            "apellido": "testLast",
            "email": "test@email.com",
            "celular": "77483362",
            "comunas": "Lo Barnechea, Santiago, Yangquihue",
            "ramos": "Matematicas, Humanidades",
            "materias": "fracciones, sumatorias, calculo",
            "instituciones": "craighouse, puc, catolica",
            "precio": 10000,
            "descripcion": "Me gustan mucho las matematicas",
            "is_teacher": True,
            "password": "pass123..",
            "password2": "pass123.."
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_email_successful(self):
        email = 'test@uc.cl'
        password = 'test'
        nombre = 'test'
        apellido = 'testlast'
        celular = '00000000'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            celular=celular
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@UC.cl'
        password = 'test'
        nombre = 'test'
        apellido = 'testlast'
        celular = '00000000'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            celular=celular
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        email = None
        password = 'test'
        nombre = 'test'
        apellido = 'testlast'
        celular = '00000000'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=email,
                password=password,
                nombre=nombre,
                apellido=apellido,
                celular=celular
            )

    def test_create_new_superuser(self):
        email = 'test1@uc.cl'
        password = 'test'
        nombre = 'test'
        apellido = 'testlast'
        celular = '00000000'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            nombre=nombre,
            apellido=apellido,
            celular=celular
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class PrivateProfileView(APITestCase):

    profile_url = reverse('get_profile')

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="email@uc.cl",
            password="pass123..",
            nombre="nombre",
            apellido="apellido",
            celular="66783359"
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

    list_profesores_url = reverse('profesors_view')
    profile_profesor_url = reverse('get_profesor', kwargs={"pk": 1})

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="email@uc.cl",
            password="pass123..",
            nombre="nombre",
            apellido="apellido",
            celular="66783359",
            is_teacher=True
        )

    def test_profile_authenticated(self):
        response = self.client.get(self.list_profesores_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_un_authenticated(self):
        response = self.client.get(self.profile_profesor_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
