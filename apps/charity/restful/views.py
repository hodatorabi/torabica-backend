from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from apps.charity.models import NonCashProjectTimeSlot
from apps.charity.restful.serializers import CharitySerializer, CashProjectSerializer, NonCashProjectSerializer, \
    NonCashProjectTimeSlotsSerializer, NonCashProjectRequestSerializer, NonCashProjectRequestResponseSerializer, \
    FeedbackSerializer
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
    serializer_class = CashProjectSerializer

    def get_queryset(self):
        return self.request.charity.cash_projects


class NonCashProjectCreateViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectSerializer

    def perform_create(self, serializer):
        serializer.save(charity=self.request.charity)


class NonCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectSerializer

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
