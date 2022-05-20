from urllib import request
from pkg_resources import require
from rest_framework import serializers
from api import models
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse


class RegisterSerializer(serializers.ModelSerializer):
    mail = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.UserProfile.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name', 'mail', 'password', 'password2', 'phone', 'comunas',
                  'assignature', 'subjects', 'institutions', 'price', 'description', 'picture', 'is_teacher')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = models.UserProfile.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'first_name', 'last_name', 'mail', 'password', 'phone', 'comunas', 'assignature',
                  'subjects', 'institutions', 'price', 'description', 'picture', 'is_teacher')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Module
        fields = ('id', 'teacher', 'start_time', 'end_time',
                  'reservation_bool', 'date', 'price')

    def create(self, validated_data):
        request = self.context.get("request", None)
        if not request:
            return

        module = models.Module.objects.create(**validated_data)
        module.save()

        return module

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'name')

    def create(self, data):
        subject = models.Subject.objects.create(**data)
        subject.save()
        return subject
