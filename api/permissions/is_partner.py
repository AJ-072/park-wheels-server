from rest_framework.permissions import BasePermission


class PartnerPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is in the client group
        return request.user.groups.filter(name='partner').exists()
