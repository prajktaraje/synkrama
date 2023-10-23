# permissions.py
from rest_framework import permissions

class IsAuthorOrSuperuser(permissions.BasePermission):
    """
    Custom permission to allow only the author and superusers to modify or delete an object.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check for object existence
            if obj:
                # Allow superusers to perform any action
                if request.user.is_superuser:
                    return True

                # Allow the author to modify or delete their own posts
                return obj.author == request.user

        # Deny access for all other cases
        return False
