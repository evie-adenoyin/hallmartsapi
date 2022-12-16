# from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
# from rest_framework.response import Response
# from rest_framework.views import APIView

# class WishListObjectPermission(BasePermission):
#     message = f"This wishlist is private, to view it set privacy in profile settings to false"
#     def has_permission(self, request, view):
#         return request.method in SAFE_METHODS

#     def has_object_permission(self, request, view, obj):
#         # Instance must have an attribute named `owner`.
#         if obj.private==True:
#             return False