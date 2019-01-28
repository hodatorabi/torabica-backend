from rest_framework.permissions import IsAuthenticated


class IsVolunteer(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if is_authenticated:
            return hasattr(request.user, 'volunteer')
        return False


class IsCharity(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if is_authenticated:
            return hasattr(request.user, 'charity')
        return False
