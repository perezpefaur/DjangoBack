from email import message
from rest_framework import permissions
from api import models
from datetime import datetime


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


class IsTimeStampAvailable(permissions.BasePermission):

    message = "You already have a module scheduled at this time"

    def has_permission(self, request, view):

        new_module = request.data

        if request.method in ["POST"]:
            query1 = models.Module.objects.filter(
                teacher_id=request.user.id,
                date=new_module["date"],
                end_time__lt=new_module["end_time"],
                end_time__gt=new_module["start_time"]
            )
            query2 = models.Module.objects.filter(
                teacher_id=request.user.id,
                date=new_module["date"],
                start_time__lt=new_module["end_time"],
                start_time__gt=new_module["start_time"]
            )

            query3 = models.Module.objects.filter(
                teacher_id=request.user.id,
                date=new_module["date"],
                start_time__lt=new_module["start_time"],
                end_time__gt=new_module["end_time"],
            )

            query4 = models.Module.objects.filter(
                teacher_id=request.user.id,
                date=new_module["date"],
                start_time=new_module["start_time"],
                end_time=new_module["end_time"],
            )

            records = query1 | query2 | query3 | query4

            return records.count() == 0
        return True

class IsPastDate(permissions.BasePermission):

    message = "The date or time you entered is in the past"

    def has_permission(self, request, view):

        new_module = request.data
        date_time_obj = datetime.strptime(new_module["date"], '%Y-%m-%d').date()
        if date_time_obj < datetime.now().date():
            return False
        return True