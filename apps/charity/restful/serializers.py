from django.db.transaction import atomic
from rest_framework import serializers

from apps.charity.models import Charity, CashProject, NonCashProject, NonCashProjectTimeSlot, CashProjectTransaction, \
    NonCashProjectRequest
from apps.volunteer.restful.serializers import PublicVolunteerSerializer
from utils.serializers import UserMixinSerializer


class CharitySerializer(UserMixinSerializer):
    class Meta:
        model = Charity
        fields = ['id', 'username', 'password', 'name', 'address', 'phone_number', 'description']
        read_only_fields = ['id']


class PublicCharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ['id', 'name', 'address', 'phone_number', 'description']
        read_only_fields = ['id', 'name', 'address', 'phone_number', 'description']


class CashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = CashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'target_amount', 'funded_amount', 'charity']
        read_only_fields = ['id', 'funded_amount', 'charity']


class NonCashProjectSerializer(serializers.ModelSerializer):
    charity = PublicCharitySerializer(read_only=True)

    class Meta:
        model = NonCashProject
        fields = ['id', 'start_date', 'end_date', 'name', 'description', 'need_male', 'need_female', 'min_age',
                  'max_age', 'city', 'abilities', 'charity']
        read_only_fields = ['id', 'charity']


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
