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

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            queryset = models.Module.objects.all()
            module = queryset.get(pk=request.GET.get("id"))
            return module.teacher_id == request.user.id
        return True


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_teacher
