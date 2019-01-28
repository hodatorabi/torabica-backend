from rest_framework import serializers

from apps.charity.models import Charity, CashProject
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

