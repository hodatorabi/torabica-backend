from django.db.transaction import atomic
from rest_framework import serializers

from apps.base_serializers import PublicVolunteerSerializer, PublicCharitySerializer
from apps.charity.models import Charity, CashProject, NonCashProject, NonCashProjectTimeSlot, CashProjectTransaction, \
    NonCashProjectRequest
from utils.serializers import UserMixinSerializer


class CharitySerializer(UserMixinSerializer):
    class Meta:
        model = Charity
        fields = ['id', 'username', 'password', 'name', 'address', 'phone_number', 'description', 'avg_rating']
        read_only_fields = ['id', 'avg_rating']


class CashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = CashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount', 'funded_amount', 'charity']
        read_only_fields = ['id', 'funded_amount', 'charity']


class CashProjectWithVolunteersSerializer(CashProjectSerializer):
    volunteers = PublicVolunteerSerializer(read_only=True, many=True)

    class Meta:
        model = CashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount', 'funded_amount', 'charity',
                  'volunteers']
        read_only_fields = ['id', 'funded_amount', 'charity', 'volunteers']


class NonCashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = NonCashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'need_male', 'need_female', 'min_age',
                  'max_age', 'city', 'abilities', 'charity']
        read_only_fields = ['id', 'charity']


class NonCashProjectWithVolunteerSerializer(NonCashProjectSerializer):
    volunteers = PublicVolunteerSerializer(read_only=True, many=True)

    class Meta:
        model = NonCashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'need_male', 'need_female', 'min_age',
                  'max_age', 'city', 'abilities', 'charity', 'volunteers']
        read_only_fields = ['id', 'charity', 'volunteers']


class NonCashProjectTimeSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCashProjectTimeSlot
        fields = ['weekday', 'time', 'project']
        read_only_fields = ['project']


class CashProjectTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashProjectTransaction
        fields = ['project', 'volunteer', 'amount']
        read_only_fields = ['project', 'volunteer']


class NonCashProjectRequestSerializer(serializers.ModelSerializer):
    project = NonCashProjectSerializer(read_only=True)
    volunteer = PublicVolunteerSerializer(read_only=True)
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = NonCashProjectRequest
        fields = ('id', 'project', 'volunteer', 'charity', 'target', 'message', 'rejection_reason', 'status')
        read_only_fields = ('id', 'project', 'volunteer', 'charity', 'target', 'rejection_reason', 'status')


class NonCashProjectRequestResponseSerializer(serializers.ModelSerializer):
    accepted = serializers.BooleanField(write_only=True)

    class Meta:
        model = NonCashProjectRequest
        fields = ('accepted', 'rejection_reason')

    @atomic
    def update(self, instance, validated_data):
        accepted = validated_data.get('accepted', False)
        validated_data['status'] = 1 if accepted else -1
        if accepted:
            instance.project.volunteers.add(instance.volunteer)
        return super().update(instance, validated_data)
