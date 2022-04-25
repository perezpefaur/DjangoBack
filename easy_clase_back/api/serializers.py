from rest_framework import serializers
from api import models

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('id', 'nombre', 'apellido', 'email', 'password', 'celular', 'comunas', 'ramos', 'materias', 'instituciones', 'precio', 'descripcion', 'is_teacher')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }
    
    def create(self, validated_data):
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            apellido=validated_data['apellido'],
            password=validated_data['password'],
            celular=validated_data['celular'],
            comunas=validated_data.get('comunas', ''),
            ramos=validated_data.get('ramos', ''),
            materias=validated_data.get('materias', ''),
            instituciones=validated_data.get('instituciones', ''),
            precio=validated_data.get('precio', ''),
            descripcion=validated_data.get('descripcion', ''),
        )
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        
        return super().update(instance, validated_data)