from rest_framework import permissions

class IsRenter(permissions.BasePermission):
    """
    Allows access only to users who are renters or staff.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_renter or request.user.is_staff))

class IsOwnerAndRenterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Also checks if the user is a renter.
    Staff members have full access.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.is_renter or request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Staff members have full access
        if request.user.is_staff:
            return True

        # Write permissions are only allowed to the owner of the item
        owner = getattr(obj, 'owner', None) or getattr(obj, 'seller', None)
        return bool(owner == request.user and request.user.is_renter)
