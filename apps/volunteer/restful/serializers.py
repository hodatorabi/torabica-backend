from rest_framework import serializers

from apps.volunteer.models import Ability, Volunteer, VolunteerTimeSlot
from utils.serializers import UserMixinSerializer


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']


class VolunteerTimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerTimeSlot
        fields = ['id', 'weekday', 'time', 'is_available', 'upcoming_project']
        read_only_fields = ['id', 'weekday', 'time', 'upcoming_project']


class VolunteerSerializer(UserMixinSerializer):
    class Meta:
        model = Volunteer
        fields = ('username', 'password', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities')


class PublicVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ('id', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities')
        read_only_fields = ('id', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities')
