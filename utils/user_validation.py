from rest_framework.permissions import BasePermission

class HasJWTUser(BasePermission):
    def has_permission(self, request, view):
        return request.user is not None