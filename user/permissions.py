from rest_framework.permissions import BasePermission


class RetrieveAndUpdateItsOwnUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
