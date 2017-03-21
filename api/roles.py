from rest_framework import permissions


class IsSpottedPage(permissions.BasePermission):
    """Permissions for SpottedPages"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='SpottedPages').exists()


class IsHarumi(permissions.BasePermission):
    """Permissions for Harumi"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Harumi').exists()
