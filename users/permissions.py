from rest_framework import permissions

class IsOwnerOnly(permissions.BasePermission):
    """
    ნებადართულია წვდომა მხოლოდ იმ მომხმარებლისთვის, ვისაც ეკუთვნის ეს პროფილი.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user