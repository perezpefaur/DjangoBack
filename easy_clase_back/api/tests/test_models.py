from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@uc.cl'
        password = 'test'
        nombre = 'test'
        apellido = 'testlast'
        celular= '00000000'
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
        celular= '00000000'
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
        celular= '00000000'
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
        celular= '00000000'
        user = get_user_model().objects.create_superuser(
            email=email, 
            password=password,
            nombre=nombre,
            apellido=apellido,
            celular=celular
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)