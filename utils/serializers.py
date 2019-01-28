from django.contrib.auth.models import User
from django.db.transaction import atomic
from rest_framework import serializers


class UserMixinSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    @atomic
    def create(self, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        validated_data['user'] = User.objects.create_user(username=username, password=password)
        return super().create(validated_data)

    @atomic
    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        password = validated_data.pop('password', None)
        if password:
            instance.user.set_password(password)
            instance.user.save()
        return super().update(instance, validated_data)
