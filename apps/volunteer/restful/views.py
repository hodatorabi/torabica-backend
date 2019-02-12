from rest_framework import generics, permissions, viewsets
from rest_framework.generics import get_object_or_404

from apps.base_serializers import PublicCashProjectSerializer, PublicNonCashProjectSerializer, PublicCharitySerializer, \
    FeedbackSerializer, PublicCharitySerializerWithFeedbacks
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
        return self.request.volunteer.cash_projects.distinct('id')


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
        queryset = CashProject.objects.all()

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        min_target = self.request.query_params.get('min_target')
        if min_target is not None:
            queryset = queryset.filter(target_amount__gte=int(min_target))

        max_target = self.request.query_params.get('max_target')
        if min_target is not None:
            queryset = queryset.filter(target_amount__lte=int(max_target))

        return queryset.distinct()


class NonCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsVolunteer]
    serializer_class = PublicNonCashProjectSerializer

    def get_queryset(self):
        queryset = NonCashProject.objects.all()

        name = self.request.query_params.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        min_age = self.request.query_params.get('min_age')
        if min_age is not None:
            queryset = queryset.filter(min_age__lte=int(min_age))

        max_age = self.request.query_params.get('max_age')
        if max_age is not None:
            queryset = queryset.filter(max_age__gte=int(max_age))

        need_male = self.request.query_params.get('need_male')
        if need_male is not None:
            queryset = queryset.filter(need_male=(need_male == 'true'))

        need_female = self.request.query_params.get('need_female')
        if need_female is not None:
            queryset = queryset.filter(need_female=(need_female == 'true'))

        city = self.request.query_params.get('city')
        if city is not None:
            queryset = queryset.filter(city__icontains=city)

        ability = self.request.query_params.get('ability')
        if ability is not None:
            queryset = queryset.filter(abilities__id=int(ability))

        weekday = self.request.query_params.get('weekday')
        if weekday is not None:
            queryset = queryset.filter(time_slots__weekday=int(weekday))

        time = self.request.query_params.get('time')
        if time is not None:
            queryset = queryset.filter(time_slots__time=int(time))

        return queryset.distinct()


class CharityViewSet(generics.RetrieveAPIView):
    queryset = Charity.objects.all()
    permission_classes = [IsVolunteer]
    serializer_class = PublicCharitySerializerWithFeedbacks
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
