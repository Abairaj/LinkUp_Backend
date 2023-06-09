from rest_framework.permissions import BasePermission


# custom permission for admin authentication
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticate and request.user.is_superuser