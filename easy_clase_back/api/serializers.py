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
                  'subjects', 'institutions', 'price', 'description', 'picture', 'is_teacher', 'is_student')
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
        fields = ('id', 'first_name', 'last_name', 'mail', 'password', 'phone', 'comunas',
                  'subjects', 'institutions', 'price', 'description', 'picture', 'is_teacher', 'is_student')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }


class ModuleSerializer(serializers.ModelSerializer):

    student_id = serializers.SerializerMethodField('student')
    reservation_id = serializers.SerializerMethodField('reservation')

    def student(self, obj):
        reservation_query = models.Reservation.objects.filter(
            module_id=obj.id
        )
        if reservation_query.count() > 0:
            return reservation_query[0].student_id

        return None

    def reservation(self, obj):
        reservation_query = models.Reservation.objects.filter(
            module_id=obj.id
        )
        if reservation_query.count() > 0:
            return reservation_query[0].id

        return None

    class Meta:
        model = models.Module
        fields = ('id', 'teacher', 'start_time', 'end_time',
                  'reservation_bool', 'date', 'student_id', 'reservation_id')
        read_only_fields = ('teacher', 'reservation_bool')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = ('id', 'name')

    def create(self, data):
        subject = models.Subject.objects.create(**data)
        subject.save()
        return subject


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institution
        fields = ('id', 'name')

    def create(self, data):
        institution = models.Institution.objects.create(**data)
        institution.save()
        return institution


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ('id', 'module', 'student', 'teacher_done', 'student_done', 'is_paid')
        read_only_fields = ('student', )

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'reservation', 'body', 'rating')