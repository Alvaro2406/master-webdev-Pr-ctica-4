from rest_framework.permissions import BasePermission
from utils.user_role import check_admin_role

class CanListUser(BasePermission):
    def has_permission(self, request, view):
        if view.action in ("list"):
            return check_admin_role(request.user)
        return True