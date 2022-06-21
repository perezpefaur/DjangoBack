# Generated by Django 3.1.8 on 2022-06-16 22:14

import api.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('mail', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=8, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{8}$')])),
                ('comunas', models.TextField(default='', max_length=255)),
                ('subjects', models.TextField(default='', max_length=255)),
                ('institutions', models.TextField(default='', max_length=255)),
                ('price', models.BigIntegerField(default=0)),
                ('description', models.CharField(default='', max_length=1000)),
                ('picture', models.ImageField(default='posts/default.png', upload_to=api.models.upload_to, verbose_name='Image')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField(validators=[api.models.min_time])),
                ('end_time', models.TimeField()),
                ('reservation_bool', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_done', models.BooleanField(default=False)),
                ('student_done', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.module')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=255)),
                ('rating', models.FloatField(default=-1)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.reservation')),
            ],
        ),
    ]
