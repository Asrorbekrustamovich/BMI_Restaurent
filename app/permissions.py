from rest_framework import permissions

class IsStaff(permissions.BasePermission):
    """
    Custom permission to only allow users with role_id=2 (staff) to access the view.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has role_id=2
        return bool(request.user and request.user.is_authenticated and 
                   getattr(request.user, 'role_id', None) == 2)