from rest_framework import generics, permissions, viewsets
from rest_framework.generics import get_object_or_404

from apps.base_serializers import PublicCashProjectSerializer, PublicNonCashProjectSerializer, PublicCharitySerializer, \
    FeedbackSerializer
from apps.charity.models import CashProject, NonCashProject, Charity
from apps.charity.restful.serializers import CashProjectTransactionSerializer, CashProjectSerializer, \
    NonCashProjectRequestSerializer, NonCashProjectRequestResponseSerializer, NonCashProjectSerializer
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


class VolunteerNonCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = NonCashProjectSerializer

    def get_queryset(self):
        return self.request.volunteer.non_cash_projects


class NonCashProjectRequestViewSet(generics.CreateAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = NonCashProjectRequestSerializer

    def perform_create(self, serializer):
        serializer.save(
            volunteer=self.request.volunteer,
            charity_id=self.kwargs.get('charity'),
            project_id=self.kwargs.get('project'),
            target=0
        )


class NonCashProjectIncomingRequestsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = NonCashProjectRequestSerializer

    def get_queryset(self):
        return self.request.volunteer.requests.filter(status=0, target=1)


class NonCashProjectOutgoingRequestsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = NonCashProjectRequestSerializer

    def get_queryset(self):
        return self.request.volunteer.requests.filter(target=0)


class NonCashProjectRequestResponseViewSet(generics.UpdateAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = NonCashProjectRequestResponseSerializer

    def get_object(self):
        return get_object_or_404(self.request.volunteer.requests, status=0, target=1, id=self.kwargs.get('request_id'))


class FeedbackViewSet(generics.CreateAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(
            volunteer=self.request.volunteer,
            charity_id=self.kwargs.get('charity'),
            target=0
        )


class FeedbacksReceivedViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return self.request.volunteer.feedbacks.filter(target=1)


class CashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = PublicCashProjectSerializer

    def get_queryset(self):
        return CashProject.objects.all()


class NonCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = PublicNonCashProjectSerializer
    queryset = NonCashProject.objects.all()


class CharityViewSet(generics.RetrieveAPIView):
    queryset = Charity.objects.all()
    permission_classes = [IsVolunteer]
    serializer_class = PublicCharitySerializer
    lookup_url_kwarg = 'charity'
    lookup_field = 'id'


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
volunteer_cash_projects_view = VolunteerCashProjectsViewSet.as_view()
volunteer_non_cash_projects_view = VolunteerNonCashProjectsViewSet.as_view()
volunteer_non_cash_project_request_view = NonCashProjectRequestViewSet.as_view()
volunteer_requests_response_view = NonCashProjectRequestResponseViewSet.as_view()
volunteer_incoming_requests_view = NonCashProjectIncomingRequestsViewSet.as_view()
volunteer_outgoing_requests_view = NonCashProjectOutgoingRequestsViewSet.as_view()
volunteer_feedback_view = FeedbackViewSet.as_view()
volunteer_feedbacks_view = FeedbacksReceivedViewSet.as_view()
cash_projects_view = CashProjectsViewSet.as_view()
non_cash_projects_view = NonCashProjectsViewSet.as_view()
show_charity_view = CharityViewSet.as_view()
