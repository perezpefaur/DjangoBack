from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
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

# Ver perfil de un profesor
class ProfesorAPIView(RetrieveAPIView):
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