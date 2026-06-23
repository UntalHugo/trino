from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Permite GET, HEAD, OPTIONS a cualquier usuario autenticado.
    Solo permite PUT, PATCH, DELETE al dueño del objeto.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user