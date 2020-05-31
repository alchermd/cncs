from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['user_permissions', 'groups', 'is_superuser', 'is_staff', 'is_active', 'date_joined']

    def to_representation(self, instance):
        rv = super(AccountSerializer, self).to_representation(instance)
        rv.pop('password', None)
        return rv

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(AccountSerializer, self).create(validated_data)
