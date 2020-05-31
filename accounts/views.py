from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import get_object_or_404
from oauth2_provider.models import Application, AccessToken
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.forms import AccountCreationForm, AccountChangeForm
from accounts.helpers import generate_tokens
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


@transaction.atomic
@api_view(['POST'])
def register(request):
    try:
        app = Application.objects.get(
            client_id=request.POST.get('client_id'),
            client_secret=request.POST.get('client_secret')
        )
    except Application.DoesNotExist:
        return Response({"detail": "Invalid client credentials."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    form = AccountCreationForm(data=request.POST)
    if form.is_valid():
        account = form.save()

        access_token, refresh_token = generate_tokens(app, account)
        response = {
            'id': account.id,
            'access_token': access_token.token,
            'refresh_token': refresh_token.token,
            'expires': access_token.expires,
            'scope': access_token.scope,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@transaction.atomic
@api_view(['POST'])
def login(request):
    try:
        app = Application.objects.get(
            client_id=request.POST.get('client_id'),
            client_secret=request.POST.get('client_secret')
        )
    except Application.DoesNotExist:
        return Response({"detail": "Invalid client credentials."}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    errors = {}
    email = request.POST.get('email')
    if not email:
        errors['email'] = 'This field is required.'

    password = request.POST.get('password')
    if not password:
        errors['password'] = 'This field is required.'

    account = authenticate(email=email, password=password)

    if account is not None:
        access_token, refresh_token = generate_tokens(app, account)

        response = {
            'id': account.id,
            'access_token': access_token.token,
            'refresh_token': refresh_token.token,
            'expires': access_token.expires,
            'scope': access_token.scope,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    else:
        return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@transaction.atomic
@api_view(['POST'])
def logout(request):
    if access_token := request.POST.get('access_token'):
        try:
            AccessToken.objects.get(token=access_token).delete()
        except AccessToken.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_204_NO_CONTENT)
