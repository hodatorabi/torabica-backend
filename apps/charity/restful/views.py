from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.charity.restful.serializers import CharitySerializer, CashProjectSerializer
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


charity_join_view = JoinCharityViewSet.as_view()
charity_profile_view = CharityProfileViewSet.as_view()
charity_cash_project_create_view = CashProjectCreateViewSet.as_view()
charity_cash_projects_view = CashProjectsViewSet.as_view()
