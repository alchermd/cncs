from datetime import datetime

from django.test import TestCase

from accounts.tests.factories import AccountFactory


class AccountModelTest(TestCase):
    def setUp(self):
        self.account = AccountFactory()

    def test_it_has_timestamp_fields(self):
        self.assertTrue(hasattr(self.account, 'created_at'))
        self.assertTrue(hasattr(self.account, 'updated_at'))

        self.assertIsInstance(self.account.created_at, datetime)
        self.assertIsInstance(self.account.updated_at, datetime)

    def test_it_has_credential_fields(self):
        self.assertTrue(hasattr(self.account, 'email'))
        self.assertIsInstance(self.account.email, str)
        self.assertTrue(hasattr(self.account, 'password'))
        self.assertIsInstance(self.account.password, str)