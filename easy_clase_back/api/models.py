import datetime
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class UserProfileManager(BaseUserManager):
    """ Manager para Perfiles de usuarios """

    def create_user(self, first_name, last_name, mail, phone, comunas='', subjects='', institutions='', price=0, description='', picture='posts/default.png', is_teacher=False, is_student=False, password=None):
        if not mail:
            raise ValueError("Usuario debe ingresar mail")

        mail = self.normalize_email(mail)
        user = self.model(mail=mail, first_name=first_name, last_name=last_name, phone=phone, comunas=comunas, subjects=subjects,
                          institutions=institutions, price=price, description=description, picture=picture, is_teacher=is_teacher, is_student=is_student)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, mail, phone, password, comunas='',  subjects='', institutions='', price=0, description='', picture='posts/default.png', is_teacher=False):
        user = self.create_user(first_name=first_name, last_name=last_name, mail=mail, phone=phone, password=password, comunas=comunas,
                                subjects=subjects, institutions=institutions, price=price, description=description, picture=picture, is_teacher=is_teacher)

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
    subjects = models.TextField(max_length=255, default='')
    institutions = models.TextField(max_length=255, default='')
    price = models.BigIntegerField(default=0)
    description = models.CharField(max_length=1000, default='')
    picture = models.ImageField(
        ("Image"), upload_to=upload_to, default='posts/default.png')

    is_student = models.BooleanField(default=False)
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
    if value < datetime.time(6, 0, 0):
        raise ValidationErr("Las clases deben partir desde las 08:00:00")


class Module(models.Model):

    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    start_time = models.TimeField(
        auto_now=False, auto_now_add=False, validators=[min_time])
    end_time = models.TimeField(
        auto_now=False, auto_now_add=False)
    reservation_bool = models.BooleanField(default=False)
    date = models.DateField()

    def create_module(self, teacher, start_time, end_time, reservation, date):
        module = Module.create(teacher=teacher, start_time=start_time,
                               end_time=end_time, reservation=reservation, date=date)
        return module


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def create_subject(self, name):
        subject = Subject.create(name=name)
        return subject


class Institution(models.Model):
    name = models.CharField(max_length=255)

    def create_institution(self, name):
        institution = Institution.create(name=name)
        return institution


class Reservation(models.Model):

    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    teacher_done = models.BooleanField(default=False)
    student_done = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def create_reservation(self, module, student, teacher_done, student_done, is_paid):
        reservation = Reservation.create(module=module, student=student, teacher_done=teacher_done, student_done=student_done, is_paid=is_paid)
        return reservation
    

class Comment(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='teacher_comments')
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='student_comments')
    body = models.CharField(max_length=255)
    rating = models.FloatField(default=-1)
    picture = models.CharField(max_length=255)
    author = models.CharField(max_length=255)


    def create_comment(self, teacher, body, rating, picture, author, student):
        comment = Comment.create(teacher=teacher, body=body, rating=rating, picture=picture, author=author, student=student)
        return comment

class Transaction(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.DO_NOTHING)
    student = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    amount = models.IntegerField(default=0)
    transaction_method = models.CharField(max_length=255)
    instance = models.DateTimeField(auto_now_add=True)

    def create_transaction(self, reservation, student, amount, transaction_method, instance):
        transaction = Transaction.create(reservation=reservation, student=student, amount=amount,  transaction_method=transaction_method, instance=instance)
        return transaction

