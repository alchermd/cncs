from rest_framework import serializers

from accounts.serializers import AccountSerializer
from snippets.models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Snippet
        exclude = ('password',)
        read_only_fields = ('key',)

    url = serializers.HyperlinkedIdentityField(view_name='snippets:snippet-detail')
    highlighted = serializers.ReadOnlyField()
    owner = AccountSerializer(required=False)
    key = serializers.CharField(read_only=True)

    def get_key(self, instance):
        return instance.key


class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('password1') != attrs.get('password2'):
            raise serializers.ValidationError('Passwords does not match')
        return attrs
