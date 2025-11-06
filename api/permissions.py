# api/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    """Allow access only to super admins."""
    def has_permission(self, request, view):
        return hasattr(request.user, "user_type") and request.user.user_type == "super_admin"


class IsAdminOrSuperAdmin(BasePermission):
    """Allow access to both admins and super admins."""
    def has_permission(self, request, view):
        if not hasattr(request.user, "user_type"):
            return False
        return request.user.user_type in ["admin", "super_admin"]


class IsVendorOrReadOnly(BasePermission):
    """Allow vendors to edit; others can only read."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return hasattr(request.user, "user_type") and request.user.user_type == "vendor"


class IsOwnerOrAdmin(BasePermission):
    """Allow owners or admins/super admins."""
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, "user_type") and request.user.user_type in ["admin", "super_admin"]:
            return True
        return hasattr(obj, "user") and obj.user == request.user
