from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.helpers import get_token_owner
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetsViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def create(self, request, *args, **kwargs):
        account = get_token_owner(request)

        if account is not None:
            serializer = SnippetSerializer(data=request.POST, context={'request': request})
            if serializer.is_valid():
                serializer.save(owner=account)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return super(SnippetsViewSet, self).create(request, *args, **kwargs)
