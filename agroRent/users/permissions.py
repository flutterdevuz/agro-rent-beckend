from rest_framework import permissions

class SuperAdminOnly(permissions.BasePermission):
    """
    Faqatgina ruxsat berilgan email egalari uchun kirish.
    """
    ALLOWED_EMAILS = [
        'arabboyazimov199@gmail.com',
        'kozimovmuhammadsodiq4472477@gmail.com'
    ]

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.email in self.ALLOWED_EMAILS or request.user.is_superuser

class IsRenter(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'is_renter', False) or getattr(request.user, 'isRenter', False)

class IsOwnerAndRenterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            (getattr(request.user, 'is_renter', False) or getattr(request.user, 'isRenter', False)) 
            and obj.owner == request.user
        )
