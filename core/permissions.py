from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_staff) or (request.method in SAFE_METHODS)


class IsAdminOrWriteOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_staff) or (request.method == "POST" and user.is_authenticated)
