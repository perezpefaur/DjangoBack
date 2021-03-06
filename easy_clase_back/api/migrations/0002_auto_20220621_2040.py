# Generated by Django 3.1.8 on 2022-06-22 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student_comments', to='api.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
