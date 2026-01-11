from rest_framework.permissions import BasePermission


class CheckRolePermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'client'


class CreateHotelPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_role == 'owner'
