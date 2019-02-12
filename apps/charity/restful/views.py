from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from apps.base_serializers import PublicVolunteerSerializer, FeedbackSerializer
from apps.charity.models import NonCashProjectTimeSlot
from apps.charity.restful.serializers import CharitySerializer, CashProjectSerializer, NonCashProjectSerializer, \
    NonCashProjectRequestSerializer, NonCashProjectRequestResponseSerializer, \
    NonCashProjectTimeSlotsSerializer, CashProjectWithVolunteersSerializer, \
    NonCashProjectWithVolunteerSerializer
from apps.volunteer.models import Volunteer
from utils.permissions import IsCharity


class JoinCharityViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CharitySerializer


class CharityProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCharity]
    serializer_class = CharitySerializer

    def get_object(self):
        return self.request.charity


class CashProjectCreateViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = CashProjectSerializer

    def perform_create(self, serializer):
        serializer.save(charity=self.request.charity)


class CashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = CashProjectWithVolunteersSerializer

    def get_queryset(self):
        return self.request.charity.cash_projects


class NonCashProjectCreateViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectSerializer

    def perform_create(self, serializer):
        serializer.save(charity=self.request.charity)


class NonCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectWithVolunteerSerializer

    def get_queryset(self):
        return self.request.charity.non_cash_projects


class NonCashProjectAddTimeSlotsViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectTimeSlotsSerializer

    def get_object(self):
        return get_object_or_404(self.request.charity.non_cash_projects, id=self.kwargs['project'])

    def perform_create(self, serializer):
        serializer.save(project=self.get_object())


class NonCashProjectTimeSlotsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectTimeSlotsSerializer

    def get_queryset(self):
        return NonCashProjectTimeSlot.objects.filter(
            project_id=self.kwargs['project'],
            project__charity_id=self.request.charity
        )


class NonCashProjectRequestViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectRequestSerializer

    def perform_create(self, serializer):
        serializer.save(
            charity=self.request.charity,
            volunteer_id=self.kwargs.get('volunteer'),
            project_id=self.kwargs.get('project'),
            target=1
        )


class NonCashProjectIncomingRequestsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectRequestSerializer

    def get_queryset(self):
        return self.request.charity.requests.filter(status=0, target=0)


class NonCashProjectOutgoingRequestsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectRequestSerializer

    def get_queryset(self):
        return self.request.charity.requests.filter(target=1)


class NonCashProjectRequestResponseViewSet(generics.UpdateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectRequestResponseSerializer

    def get_object(self):
        return get_object_or_404(self.request.charity.requests, status=0, target=0, id=self.kwargs.get('request_id'))


class FeedbackViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(
            charity=self.request.charity,
            volunteer_id=self.kwargs.get('volunteer'),
            target=1
        )


class FeedbacksReceivedViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        return self.request.charity.feedbacks.filter(target=0)


class VolunteersViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = PublicVolunteerSerializer

    def get_queryset(self):
        queryset = Volunteer.objects.all()

        min_age = self.request.query_params.get('min_age')
        if min_age is not None:
            queryset = queryset.filter(age__gte=int(min_age))

        max_age = self.request.query_params.get('max_age')
        if max_age is not None:
            queryset = queryset.filter(age__lte=int(max_age))

        city = self.request.query_params.get('city')
        if city is not None:
            queryset = queryset.filter(city__icontains=city)

        gender = self.request.query_params.get('gender')
        if gender is not None:
            queryset = queryset.filter(gender=gender)

        ability = self.request.query_params.get('ability')
        if ability is not None:
            queryset = queryset.filter(abilities__id=int(ability))

        weekday = self.request.query_params.get('weekday')
        if weekday is not None:
            queryset = queryset.filter(time_slots__weekday=int(weekday), time_slots__is_available=True)

        time = self.request.query_params.get('time')
        if time is not None:
            queryset = queryset.filter(time_slots__time=int(time), time_slots__is_available=True)

        return queryset.distinct()


charity_join_view = JoinCharityViewSet.as_view()
charity_profile_view = CharityProfileViewSet.as_view()
charity_cash_project_create_view = CashProjectCreateViewSet.as_view()
charity_cash_projects_view = CashProjectsViewSet.as_view()
charity_non_cash_project_create_view = NonCashProjectCreateViewSet.as_view()
charity_non_cash_projects_view = NonCashProjectsViewSet.as_view()
charity_non_cash_project_add_time_slot_view = NonCashProjectAddTimeSlotsViewSet.as_view()
charity_non_cash_project_time_slots_view = NonCashProjectTimeSlotsViewSet.as_view()
charity_non_cash_project_request_view = NonCashProjectRequestViewSet.as_view()
charity_requests_response_view = NonCashProjectRequestResponseViewSet.as_view()
charity_incoming_requests_view = NonCashProjectIncomingRequestsViewSet.as_view()
charity_outgoing_requests_view = NonCashProjectOutgoingRequestsViewSet.as_view()
charity_feedback_view = FeedbackViewSet.as_view()
charity_feedbacks_view = FeedbacksReceivedViewSet.as_view()
volunteers_view = VolunteersViewSet.as_view()
