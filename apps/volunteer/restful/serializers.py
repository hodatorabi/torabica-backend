from rest_framework import serializers

from apps.base_serializers import PublicNonCashProjectSerializer
from apps.volunteer.models import Ability, Volunteer, VolunteerTimeSlot
from utils.serializers import UserMixinSerializer


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']


class VolunteerTimeSlotsSerializer(serializers.ModelSerializer):
    upcoming_project = PublicNonCashProjectSerializer(read_only=True)

    class Meta:
        model = VolunteerTimeSlot
        fields = ['id', 'weekday', 'time', 'is_available', 'upcoming_project']
        read_only_fields = ['id', 'weekday', 'time', 'upcoming_project']


class VolunteerSerializer(UserMixinSerializer):
    class Meta:
        model = Volunteer
        fields = ('username', 'password', 'name', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities')
