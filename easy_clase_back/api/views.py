from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from api import permissions
from .serializers import RegisterSerializer, UserSerializer, ModuleSerializer
from django_filters import rest_framework as filters
from api.filters import TeachersFilter, ModulesFilter
from api import models
import json


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# La lista de todos los Prosefores es publico


class TeachersAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_teacher=True)
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TeachersFilter

# Ver perfil de un profesor


class TeacherAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_teacher=True)
    permission_classes = (AllowAny,)

# Ver mi propio perfil


class PerfilAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, permissions.IsOwnerOrReadOnly]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj


# Lista de Modules"""
class ModulesAPIView(generics.ListAPIView):
    queryset = models.Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ModulesFilter


# Borrar módulo
class ModuleAPIView(generics.CreateAPIView, RetrieveUpdateDestroyAPIView):

    queryset = models.Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, permissions.IsModuleOwner]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.query_params.get("id"))
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        body = json.loads(request.body)
        teacher = body['teacher']
        if teacher != request.user.id or not request.user.is_teacher:
            return HttpResponse('Unauthorized', status=401)
        else: 
            return super().create(request, *args, **kwargs)