from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    创建者权限验证
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
