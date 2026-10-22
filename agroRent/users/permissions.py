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

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    O'qish hammaga, yaratish/o'zgartirish/o'chirish faqat staff (admin) uchun.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class IsRenter(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_staff or getattr(request.user, 'is_renter', False)

class IsOwnerAndRenterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        # RentItem'da egasi `owner`, MarketItem'da esa `seller`
        owner = getattr(obj, 'owner', None) or getattr(obj, 'seller', None)
        return getattr(request.user, 'is_renter', False) and owner == request.user
