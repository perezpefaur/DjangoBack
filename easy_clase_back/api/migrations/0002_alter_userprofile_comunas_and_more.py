# Generated by Django 4.0.4 on 2022-04-25 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='comunas',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='descripcion',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='instituciones',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='materias',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='ramos',
            field=models.TextField(default='', max_length=255),
        ),
    ]
