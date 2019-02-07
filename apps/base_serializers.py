from rest_framework import serializers

from apps.charity.models import Charity, CashProject, NonCashProject, NonCashProjectTimeSlot, Feedback
from apps.volunteer.models import VolunteerTimeSlot, Volunteer


class PublicCharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ['id', 'name', 'address', 'phone_number', 'description', 'avg_rating']
        read_only_fields = ['id', 'name', 'address', 'phone_number', 'description', 'avg_rating']


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


class PublicFeedbackSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'charity', 'comment', 'rating']
        read_only_fields = ['id', 'charity', 'comment', 'rating']


class PublicVolunteerSerializer(serializers.ModelSerializer):
    received_feedback = PublicFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = Volunteer
        fields = (
            'id', 'username', 'name', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities',
            'avg_rating', 'received_feedback')
        read_only_fields = (
            'id', 'username', 'name', 'gender', 'age', 'phone_number', 'address', 'city', 'abilities',
            'avg_rating', 'received_feedback')


class PublicCharitySerializerWithFeedbacks(serializers.ModelSerializer):
    received_feedback = PublicFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = Charity
        fields = ('id', 'username', 'name', 'address', 'phone_number', 'description', 'avg_rating', 'received_feedback')
        read_only_fields = (
            'id', 'username', 'name', 'address', 'phone_number', 'description', 'avg_rating', 'received_feedback')


class PublicCashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = CashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount', 'funded_amount', 'charity']
        read_only_fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount',
                            'funded_amount', 'charity']


class FeedbackSerializer(serializers.ModelSerializer):
    volunteer = PublicVolunteerSerializer(read_only=True)
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'charity', 'volunteer', 'target', 'comment', 'rating']
        read_only_fields = ['id', 'charity', 'volunteer', 'target']
