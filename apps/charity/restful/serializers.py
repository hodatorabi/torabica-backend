from rest_framework import serializers

from apps.charity.models import Charity, CashProject, NonCashProject, NonCashProjectTimeSlot, CashProjectTransaction
from utils.serializers import UserMixinSerializer


class CharitySerializer(UserMixinSerializer):
    class Meta:
        model = Charity
        fields = ('username', 'password', 'name', 'address', 'phone_number', 'description')


class CashProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashProject
        fields = ['start_date', 'end_date', 'name', 'description', 'target_amount', 'funded_amount']
        read_only_fields = ['funded_amount']


class NonCashProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonCashProject
        fields = ['start_date', 'end_date', 'name', 'description', 'need_male', 'need_female', 'min_age', 'max_age',
                  'city', 'abilities']


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
