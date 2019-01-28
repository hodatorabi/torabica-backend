from rest_framework.permissions import IsAuthenticated


class IsVolunteer(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if is_authenticated:
            volunteer = getattr(request.user, 'volunteer', None)
            if volunteer:
                setattr(request, 'volunteer', volunteer)
            return bool(volunteer)
        return False


class IsCharity(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if is_authenticated:
            charity = getattr(request.user, 'charity', None)
            if charity:
                setattr(request, 'charity', charity)
            return bool(charity)
        return False
