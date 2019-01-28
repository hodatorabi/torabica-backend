from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

from apps.charity.models import NonCashProjectTimeSlot
from apps.charity.restful.serializers import CharitySerializer, CashProjectSerializer, NonCashProjectSerializer, \
    NonCashProjectTimeSlotsSerializer
from utils.permissions import IsCharity


class JoinCharityViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CharitySerializer


class CharityProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCharity]
    serializer_class = CharitySerializer

    def get_object(self):
        return self.request.user.charity


class CashProjectCreateViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = CashProjectSerializer

    def perform_create(self, serializer):
        serializer.save(charity=self.request.user.charity)


class CashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = CashProjectSerializer

    def get_queryset(self):
        return self.request.user.charity.cash_projects


class NonCashProjectCreateViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectSerializer

    def perform_create(self, serializer):
        serializer.save(charity=self.request.user.charity)


class NonCashProjectsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectSerializer

    def get_queryset(self):
        return self.request.user.charity.non_cash_projects


class NonCashProjectAddTimeSlotsViewSet(generics.CreateAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectTimeSlotsSerializer

    def get_object(self):
        return get_object_or_404(self.request.user.charity.non_cash_projects, id=self.kwargs['project'])

    def perform_create(self, serializer):
        serializer.save(project=self.get_object())


class NonCashProjectTimeSlotsViewSet(generics.ListAPIView):
    permission_classes = [IsCharity]
    serializer_class = NonCashProjectTimeSlotsSerializer

    def get_queryset(self):
        return NonCashProjectTimeSlot.objects.filter(
            project_id=self.kwargs['project'],
            project__charity_id=self.request.user.charity
        )


charity_join_view = JoinCharityViewSet.as_view()
charity_profile_view = CharityProfileViewSet.as_view()
charity_cash_project_create_view = CashProjectCreateViewSet.as_view()
charity_cash_projects_view = CashProjectsViewSet.as_view()
non_charity_cash_project_create_view = NonCashProjectCreateViewSet.as_view()
non_charity_cash_projects_view = NonCashProjectsViewSet.as_view()
charity_non_cash_project_add_time_slot_view = NonCashProjectAddTimeSlotsViewSet.as_view()
charity_non_cash_project_time_slots_view = NonCashProjectTimeSlotsViewSet.as_view()
