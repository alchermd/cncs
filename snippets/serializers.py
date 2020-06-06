from rest_framework import serializers

from accounts.serializers import AccountSerializer
from snippets.models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Snippet
        fields = '__all__'

    url = serializers.HyperlinkedIdentityField(view_name='snippets:snippet-detail')
    highlighted = serializers.ReadOnlyField()
    owner = AccountSerializer(required=False)


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError('Passwords does not match')
        return attrs
