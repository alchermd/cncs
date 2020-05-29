import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.managers import AccountManager
from snippets.models import TimestampedModel


class Account(AbstractUser, TimestampedModel):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    # Custom fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)

    # Removed fields
    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email
