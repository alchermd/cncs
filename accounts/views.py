from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.forms import AccountCreationForm, AccountChangeForm
from accounts.models import Account
from accounts.serializers import AccountSerializer


@transaction.atomic
@api_view(['GET', 'POST', ])
def account_list(request):
    context = {'request': request}

    if request.method == 'GET':
        serializer = AccountSerializer(Account.objects.all(), many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        form = AccountCreationForm(data=request.POST)
        if form.is_valid():
            account = form.save()
            serializer = AccountSerializer(instance=account, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors.as_json(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@transaction.atomic
@api_view(['GET', 'PATCH', 'DELETE', ])
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=pk)
    context = {'request': request}

    if request.method == 'GET':
        serializer = AccountSerializer(instance=account, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        form = AccountChangeForm(instance=account, data=request.POST)
        if form.is_valid():
            account = form.save()
            serializer = AccountSerializer(instance=account, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors.as_json(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
