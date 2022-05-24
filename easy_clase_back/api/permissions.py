from email import message
from rest_framework import permissions
from api import models


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the movie
        return obj.id == request.user.id


class IsModuleOwner(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    message = "You are not the owner of this module"

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            queryset = models.Module.objects.all()
            module = queryset.get(pk=request.GET.get("id"))
            return module.teacher_id == request.user.id
        return True


class IsModuleReservated(permissions.BasePermission):

    message = "This module is already taken"

    def has_permission(self, request, view):
        if request.method in ["POST"]:
            queryset = models.Module.objects.all()
            module = queryset.get(pk=request.data["module"])

            if module.reservation_bool:
                return False
            else:
                module.reservation_bool = True
                module.save()
                return True
        return True


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_student


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_teacher
