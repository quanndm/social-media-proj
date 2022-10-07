from rest_framework import permissions
class userPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        method = ("GET", "PUT", "DELETE", "PATCH")
        if request.method in method and request.user.is_authenticated:
            return True
        if request.method == "POST":
            return True