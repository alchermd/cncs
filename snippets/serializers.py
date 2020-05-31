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
