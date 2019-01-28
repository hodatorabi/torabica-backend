from apps.charity.models import Charity
from utils.serializers import UserMixinSerializer


class CharitySerializer(UserMixinSerializer):
    class Meta:
        model = Charity
        fields = ('username', 'password', 'name', 'address', 'phone_number', 'description')
