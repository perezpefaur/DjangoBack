
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from api import permissions
from .serializers import RegisterSerializer, ReservationSerializer, UserSerializer, ModuleSerializer, SubjectSerializer, InstitutionSerializer, CommentSerializer, TransactionSerializer
from django_filters import rest_framework as filters
from api.filters import TeachersFilter, ModulesFilter, SubjectsFilter, InstitutionsFilter, CommentsFilter
from api import models
from rest_framework.response import Response
from rest_framework import status


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save()

        if serializer.validated_data['is_teacher']:
            subjects = serializer.validated_data['subjects']
            subjects = subjects.split(',')
            for subject in subjects:
                if not models.Subject.objects.filter(name=subject).exists():
                    models.Subject.objects.create(name=subject)

            institutions = serializer.validated_data['institutions']
            institutions = institutions.split(',')
            for institution in institutions:
                if not models.Institution.objects.filter(name=institution).exists():
                    models.Institution.objects.create(name=institution)
        return

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


# Crear, Get, Update y Borrar módulo
class ModuleAPIView(generics.CreateAPIView, RetrieveUpdateDestroyAPIView):

    queryset = models.Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, permissions.IsModuleOwner, permissions.IsTeacher,
                          permissions.IsTimeStampAvailable, permissions.IsPastDate,
                          permissions.StartTimeBeforeEndTime]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        module = queryset.get(pk=self.request.query_params.get("id"))
        return module

    def perform_create(self, serializer):
        # The request user is set as author automatically.
        serializer.save(teacher=self.request.user)
        return


class ReservationAPIView(generics.CreateAPIView, RetrieveUpdateDestroyAPIView):

    queryset = models.Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, permissions.IsModuleReservated, permissions.IsStudent,
                          permissions.checkStudentClassConfirmation, permissions.checkTeacherClassConfirmation]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        reservation = queryset.get(pk=self.request.query_params.get("id"))
        self.check_object_permissions(self.request, reservation)
        return reservation

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        return

    def destroy(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        reservation = queryset.get(pk=self.request.query_params.get("id"))
        module = reservation.module
        module.reservation_bool = False
        module.save()
        return super().destroy(request, *args, **kwargs)

# Crear subject


class SubjectAPIView(generics.CreateAPIView):

    queryset = models.Subject.objects.all()
    serializer_class = SubjectSerializer


# Lista de subjects
class SubjectsAPIView(generics.ListAPIView):
    serializer_class = SubjectSerializer
    queryset = models.Subject.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SubjectsFilter

# Crear institution


class InstitutionAPIView(generics.CreateAPIView):

    queryset = models.Institution.objects.all()
    serializer_class = InstitutionSerializer


# Lista de institutions
class InstitutionsAPIView(generics.ListAPIView):
    serializer_class = InstitutionSerializer
    queryset = models.Institution.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InstitutionsFilter

# Crear, editar, borrar comentario


class CommentAPIView(generics.CreateAPIView, RetrieveUpdateDestroyAPIView):

    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, permissions.IsStudent,
                          permissions.hasReservationWithTeacher, permissions.isCommentOwner]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        comment = queryset.get(pk=self.request.query_params.get("id"))
        self.check_object_permissions(self.request, comment)
        return comment

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.first_name + " " + self.request.user.last_name, picture=self.request.user.picture, student=self.request.user)
        return

# Lista de comentarios


class CommentsAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentsFilter

# Crear, editar, borrar comentario


class TransactionAPIView(generics.CreateAPIView, RetrieveUpdateDestroyAPIView):

    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, permissions.IsStudent,
                          permissions.isReservationOwner, permissions.isTransactionOwner]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        comment = queryset.get(pk=self.request.query_params.get("id"))
        self.check_object_permissions(self.request, comment)
        return comment

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
        return


class TransactionsAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = models.Transaction.objects.all()
    permission_classes = (AllowAny,)


class ReservationCheckAPIView(generics.RetrieveAPIView):

    serializer_class = ReservationSerializer
    queryset = models.Reservation.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request):
        queryset = models.Reservation.objects.filter(
            module__teacher=self.request.query_params.get("teacher_id")).filter(student=self.request.query_params.get("student_id"))

        result = len(queryset) > 0
        return Response({'checkReservation': result}, status=status.HTTP_200_OK)
