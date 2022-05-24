from rest_framework import permissions


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
        return obj["teacher"] == request.user.id

    def has_permission(self, request, view):
        if type(request.data) == list():
            permList = list(map(lambda perm: self.has_object_permission(
                request, view, perm), request.data))
            return all(permList)
        return request.data["teacher"] == request.user.id


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request.user.is_teacher)
        return request.user.is_teacher
