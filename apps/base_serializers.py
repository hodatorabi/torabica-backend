from rest_framework import serializers

from apps.charity.models import Charity, CashProject, NonCashProject, NonCashProjectTimeSlot
from apps.volunteer.models import VolunteerTimeSlot, Volunteer


class PublicCharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ['id', 'name', 'address', 'phone_number', 'description']
        read_only_fields = ['id', 'name', 'address', 'phone_number', 'description']


class PublicNonCashProjectTimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCashProjectTimeSlot
        fields = ['weekday', 'time', 'project']
        read_only_fields = ['weekday', 'time', 'project']


class PublicNonCashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)
    time_slots = PublicNonCashProjectTimeSlotsSerializer(read_only=True, many=True)

    class Meta:
        model = NonCashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'need_male', 'need_female', 'min_age',
                  'max_age', 'city', 'abilities', 'charity', 'time_slots']
        read_only_fields = ['id', 'start_date', 'end_date', 'name', 'description', 'need_male', 'need_female',
                            'min_age', 'max_age', 'city', 'abilities', 'charity', 'time_slots']


class PublicVolunteerTimeSlotsSerializer(serializers.ModelSerializer):
    upcoming_project = PublicNonCashProjectSerializer(read_only=True)

    class Meta:
        model = VolunteerTimeSlot
        fields = ['id', 'weekday', 'time', 'is_available', 'upcoming_project']
        read_only_fields = ['id', 'weekday', 'time', 'is_available', 'upcoming_project']


class PublicVolunteerSerializer(serializers.ModelSerializer):
    time_slots = PublicVolunteerTimeSlotsSerializer(read_only=True, many=True)

    class Meta:
        model = Volunteer
        fields = (
            'id', 'username', 'name', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities', 'time_slots')
        read_only_fields = (
            'id', 'username', 'name', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities', 'time_slots')


class PublicCashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = CashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount', 'funded_amount', 'charity']
        read_only_fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount',
                            'funded_amount', 'charity']
