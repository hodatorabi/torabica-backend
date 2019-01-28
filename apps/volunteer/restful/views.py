from rest_framework import generics, permissions, viewsets

from apps.charity.restful.serializers import CashProjectTransactionSerializer, CashProjectSerializer
from apps.volunteer.models import Ability
from apps.volunteer.restful.serializers import AbilitySerializer, VolunteerSerializer, VolunteerTimeSlotsSerializer
from utils.permissions import IsVolunteer


class VolunteerJoinViewSet(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VolunteerSerializer


class VolunteerProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = VolunteerSerializer

    def get_object(self):
        return self.request.volunteer


class VolunteerTimeSlotsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsVolunteer]
    serializer_class = VolunteerTimeSlotsSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return self.request.volunteer.time_slots


class AbilitiesViewSet(generics.ListAPIView):
    serializer_class = AbilitySerializer
    queryset = Ability.objects.all()


class CashProjectTransactionViewSet(generics.CreateAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = CashProjectTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(volunteer=self.request.volunteer, project_id=self.kwargs['project'])


class VolunteerCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = CashProjectSerializer

    def get_queryset(self):
        return self.request.volunteer.cash_projects


volunteer_join_view = VolunteerJoinViewSet.as_view()
volunteer_profile_view = VolunteerProfileViewSet.as_view()
volunteer_time_slots_view = VolunteerTimeSlotsViewSet.as_view({'get': 'list'})
volunteer_time_slot_update_view = VolunteerTimeSlotsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update'
})
abilities_view = AbilitiesViewSet.as_view()
cash_project_create_transaction = CashProjectTransactionViewSet.as_view()
cash_projects_view = VolunteerCashProjectsViewSet.as_view()
