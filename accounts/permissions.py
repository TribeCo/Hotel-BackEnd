from rest_framework.permissions import BasePermission
#-----------------------------------------------------------
class IsHotelManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'm':
            return True

        return False
#-----------------------------------------------------------
class IsDeputy(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'd':
            return True

        return False
#-----------------------------------------------------------
class IsAssentManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'a':
            return True

        return False
#-----------------------------------------------------------
class IsRestaurantManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role == 'r':
            return True

        return False
#-----------------------------------------------------------
class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.role in ['m','d','a','r']:
            return True

        return False
#-----------------------------------------------------------

