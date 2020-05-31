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