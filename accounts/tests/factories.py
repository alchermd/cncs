import factory
from django.contrib.auth.hashers import make_password
from oauth2_provider.models import Application

from accounts.models import Account


class AccountFactory(factory.DjangoModelFactory):
    class Meta:
        model = Account

    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password(factory.Faker('password')))


class ApplicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Application

    user = factory.SubFactory(AccountFactory)
