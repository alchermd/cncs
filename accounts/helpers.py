from datetime import timedelta

from django.utils import timezone
from oauth2_provider.models import AccessToken, RefreshToken
from oauthlib.common import generate_token


def generate_tokens(app, account):
    """
    Generate Access and Refresh tokens for an oauth2 app's account
    """
    next_week = timezone.now() + timedelta(weeks=1)
    access_token = AccessToken.objects.create(application=app, user=account, scope='read write',
                                              token=generate_token(),
                                              expires=next_week)
    refresh_token = RefreshToken.objects.create(application=app, user=account, access_token=access_token,
                                                token=generate_token())
    return access_token, refresh_token


def get_token_owner(request, identifier='Bearer'):
    """
    Fetches the owner of the request's access token
    """
    try:
        if not (auth_string := request.headers.get('AUTHORIZATION')):
            return None

        access_token = auth_string[len(identifier) + 1:]
        return AccessToken.objects.get(token=access_token).user
    except AccessToken.DoesNotExist:
        return None
