from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorModeratorAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):

        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):

        return (obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)


class ReadOrAdminOnly(BasePermission):
    """Доступ админу к действиям над объектом."""
    def has_permission(self, request, view):

        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))


class AdminOnly(BasePermission):
    def has_permission(self, request, view):

        return (request.user.is_authenticated
                and request.user.is_admin)
