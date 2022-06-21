from email import message
from rest_framework import permissions
from api import models
import json
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
    message = "You must be a student to perform this action"

    def has_permission(self, request, view):
        if request.method != "PATCH":
            return request.user.is_student
        return True


class IsTeacher(permissions.BasePermission):
    message = "You must be a teacher to perform this action"

    def has_permission(self, request, view):
        return request.user.is_teacher


class isReservationOwner(permissions.BasePermission):
    message = "You are not the owner of this reservation"

    def has_permission(self, request, view):
        if request.method in ["POST"]:
            queryset = models.Reservation.objects.all()
            reservation_id = json.loads(request.body)['reservation']
            reservation = queryset.get(pk=reservation_id)
            return reservation.student_id == request.user.id
        return True


class didHappen(permissions.BasePermission):
    message = "The student or teacher has not confirmed that this class happened"

    def has_permission(self, request, view):
        if request.method in ["POST"]:
            queryset = models.Reservation.objects.all()
            reservation_id = json.loads(request.body)['reservation']
            reservation = queryset.get(pk=reservation_id)
            return reservation.teacher_done & reservation.student_done
        return True


class isCommentOwner(permissions.BasePermission):
    message = "You are not the owner of this comment"

    def has_permission(self, request, view):
        if request.method in ["PATCH", "DELETE"]:
            queryset = models.Comment.objects.all()
            comment = queryset.get(pk=request.GET.get("id"))
            queryset2 = models.Reservation.objects.all()
            reservation = queryset2.get(pk=comment.reservation_id)
            return reservation.student_id == request.user.id
        return True


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

        if request.method == "POST":
            new_module = request.data
            date_time_obj = datetime.strptime(
                new_module["date"] + " " + new_module["start_time"], '%Y-%m-%d %H:%M:%S')
            if date_time_obj < datetime.now():
                return False
            return True

        elif request.method == "PATCH":
            try:
                new_module = request.data
                date_time_obj = datetime.strptime(
                    new_module["date"] + " " + new_module["start_time"], '%Y-%m-%d %H:%M:%S')
                if date_time_obj < datetime.now():
                    return False
                return True
            except KeyError:
                return True

        return True


class StartTimeBeforeEndTime(permissions.BasePermission):

    message = "The start time must be before the end time"

    def has_permission(self, request, view):

        if request.method == "POST":
            new_module = request.data
            date_time_obj = datetime.strptime(
                new_module["date"] + " " + new_module["start_time"], '%Y-%m-%d %H:%M:%S')
            date_time_obj2 = datetime.strptime(
                new_module["date"] + " " + new_module["end_time"], '%Y-%m-%d %H:%M:%S')
            if date_time_obj2 <= date_time_obj:
                return False
            return True

        elif request.method == "PATCH":
            try:
                new_module = request.data
                date_time_obj = datetime.strptime(
                    new_module["date"] + " " + new_module["start_time"], '%Y-%m-%d %H:%M:%S')
                date_time_obj2 = datetime.strptime(
                    new_module["date"] + " " + new_module["end_time"], '%Y-%m-%d %H:%M:%S')
                if date_time_obj2 <= date_time_obj:
                    return False
                return True
            except KeyError:
                return True

        return True


class checkTeacherClassConfirmation(permissions.BasePermission):

    message = "You must be the teacher to confirm this class"

    def has_permission(self, request, view):

        if request.method in ["PATCH", "POST"]:
            try:
                if request.data["teacher_done"]:
                    return request.user.is_teacher
            except KeyError:
                return True
        return True


class checkStudentClassConfirmation(permissions.BasePermission):

    message = "You must be the student to confirm this class"

    def has_permission(self, request, view):

        if request.method in ["PATCH", "POST"]:
            try:
                if request.data["student_done"]:
                    return request.user.is_student
            except KeyError:
                return True
        return True


class isTransactionOwner(permissions.BasePermission):
    message = "You are not the owner of this transaction"

    def has_object_permission(self, request, view, obj):
        if request.method in ["PATCH", "DELETE"]:
            queryset = models.Transaction.objects.all()
            transaction = queryset.get(pk=request.GET.get("id"))
            return transaction.student_id == request.user.id
        return True
