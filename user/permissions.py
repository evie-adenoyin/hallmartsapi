from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class UserObjectPermission(BasePermission):
    # message = f"Login in to access this page"
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    
    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        if request.method in SAFE_METHODS and obj.user == request.user:
            return True