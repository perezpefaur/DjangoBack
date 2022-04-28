from rest_framework import serializers
from api import models
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=models.UserProfile.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.UserProfile
        fields = ('id', 'nombre', 'apellido', 'email', 'password', 'password2', 'celular', 'comunas',
                  'ramos', 'materias', 'instituciones', 'precio', 'descripcion', 'imagen', 'is_teacher')
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
        fields = ('id', 'nombre', 'apellido', 'email', 'password', 'celular', 'comunas', 'ramos',
                  'materias', 'instituciones', 'precio', 'descripcion', 'imagen', 'is_teacher')
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
        fields = ('id', 'profesor', 'start_time', 'end_time',
                  'reservationBool', 'date')
