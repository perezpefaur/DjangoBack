from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from api import permissions
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# La lista de Prosefores es publico
class ProfesorsAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_teacher=True)
    permission_classes = (AllowAny,)