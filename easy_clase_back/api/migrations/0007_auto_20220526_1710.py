# Generated by Django 3.1.8 on 2022-05-26 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_merge_20220524_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_student',
            field=models.BooleanField(default=False),
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
