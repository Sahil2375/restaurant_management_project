# permissions.py
from rest_framework import permissions

class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'driver')  # Checks if user is a driver

class IsRideRiderOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.rider or request.user.is_staff
