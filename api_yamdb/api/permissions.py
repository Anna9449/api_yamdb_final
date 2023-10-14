from rest_framework import permissions


class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (request.user.is_admin
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in permissions.SAFE_METHODS
        return (request.user.is_admin
                or request.user.is_superuser
                or request.method in permissions.SAFE_METHODS)
