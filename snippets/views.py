from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from oauth2_provider.decorators import protected_resource
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.helpers import get_token_owner, get_password_token
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, PasswordSerializer


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

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        snippet = get_object_or_404(Snippet, pk=pk)

        if snippet.password:
            password = get_password_token(request)
            password_is_invalid = password is None or not check_password(password, snippet.password)

            account = get_token_owner(request)
            token_is_invalid = snippet.owner != account

            if password_is_invalid and token_is_invalid:
                return Response({'detail': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        return super(SnippetsViewSet, self).retrieve(request, *args, **kwargs)


@transaction.atomic()
@protected_resource()
@api_view(['POST'])
def set_password(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    context = {'request': request}

    serializer = PasswordSerializer(data=request.data)
    if serializer.is_valid():
        snippet.set_password(serializer.data['password1'])
        snippet.save()
        return Response(SnippetSerializer(instance=snippet, context=context).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
