from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class UserProfileManager(BaseUserManager):
    """ Manager para Perfiles de usuarios """

    def create_user(self, nombre, apellido, email, celular, comunas='', ramos='', materias='', instituciones='', precio=0, descripcion='', imagen='posts/default.png', is_teacher=False, password=None):
        if not email:
            raise ValueError("Usuario debe ingresar mail")

        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, celular=celular, comunas=comunas, ramos=ramos, materias=materias,
                          instituciones=instituciones, precio=precio, descripcion=descripcion, imagen=imagen, is_teacher=is_teacher)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, nombre, apellido, email, celular, password, comunas='', ramos='', materias='', instituciones='', precio=0, descripcion='', imagen='posts/default.png', is_teacher=False):
        user = self.create_user(nombre, apellido, email, celular, comunas, ramos,
                                materias, instituciones, precio, descripcion, imagen, is_teacher, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    celular = models.CharField(max_length=8, unique=True, validators=[
                               RegexValidator(r'^[0-9]{8}$')])
    comunas = models.TextField(max_length=255, default='')
    ramos = models.TextField(max_length=255, default='')
    materias = models.TextField(max_length=255, default='')
    instituciones = models.TextField(max_length=255, default='')
    precio = models.BigIntegerField(default=0)
    descripcion = models.CharField(max_length=1000, default='')
    imagen = models.ImageField(
        ("Image"), upload_to=upload_to, default='posts/default.png')

    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'celular']

    def get_full_name(self):
        return self.nombre + self.apellido

    def get_short_name(self):
        return self.nombre

    def __str__(self):
        return self.email


class Module(models.Model):
    profesor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    reservationBool = models.BooleanField()
    date = models.DateField()
