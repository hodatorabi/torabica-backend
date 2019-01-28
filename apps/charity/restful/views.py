from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.charity.restful.serializers import CharitySerializer
from utils.permissions import IsCharity


class JoinCharityViewSet(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CharitySerializer


class CharityProfileViewSet(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCharity]
    serializer_class = CharitySerializer

    def get_object(self):
        return self.request.user.charity


charity_join_view = JoinCharityViewSet.as_view()
charity_profile_view = CharityProfileViewSet.as_view()
