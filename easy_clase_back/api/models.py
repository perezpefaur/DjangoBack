import datetime
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class UserProfileManager(BaseUserManager):
    """ Manager para Perfiles de usuarios """

    def create_user(self, first_name, last_name, mail, phone, comunas='', assignature='', subjects='', institutions='', price=0, description='', picture='posts/default.png', is_teacher=False, password=None):
        if not mail:
            raise ValueError("Usuario debe ingresar mail")

        mail = self.normalize_email(mail)
        user = self.model(mail=mail, first_name=first_name, last_name=last_name, phone=phone, comunas=comunas, assignature=assignature, subjects=subjects,
                          institutions=institutions, price=price, description=description, picture=picture, is_teacher=is_teacher)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, mail, phone, password, comunas='', assignature='', subjects='', institutions='', price=0, description='', picture='posts/default.png', is_teacher=False):
        user = self.create_user(first_name, last_name, mail, phone, comunas, assignature,
                                subjects, institutions, price, description, picture, is_teacher, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mail = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=8, unique=True, validators=[
        RegexValidator(r'^[0-9]{8}$')])
    comunas = models.TextField(max_length=255, default='')
    assignature = models.TextField(max_length=255, default='')
    subjects = models.TextField(max_length=255, default='')
    institutions = models.TextField(max_length=255, default='')
    price = models.BigIntegerField(default=0)
    description = models.CharField(max_length=1000, default='')
    picture = models.ImageField(
        ("Image"), upload_to=upload_to, default='posts/default.png')

    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.mail


def min_time(value):
    if value < datetime.time(8, 0, 0):
        raise ValidationErr("Las clases deben partir desde las 08:00:00")


def max_time(value):
    if value > datetime.time(23, 0, 0):
        raise ValidationErr("Las clases no deben terminar pasado las 23:00:00")


class Module(models.Model):

    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_time = models.TimeField(
        auto_now=False, auto_now_add=False, validators=[min_time])
    end_time = models.TimeField(
        auto_now=False, auto_now_add=False, validators=[max_time])
    reservation_bool = models.BooleanField()
    date = models.DateField()
    price = models.IntegerField()

    def create_module(self, teacher, start_time, end_time, reservation, date):
        module = Module.create(teacher=teacher, start_time=start_time,
                               end_time=end_time, reservation=reservation, date=date)
        return module
