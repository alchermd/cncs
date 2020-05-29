from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import Account
from accounts.tests.factories import AccountFactory


class AccountsViewsTest(APITestCase):
    def test_can_browse_all_accounts(self):
        AccountFactory.create_batch(3)

        response = self.client.get(reverse('accounts:account-list'))

        self.assertEquals(200, response.status_code)
        self.assertEquals(3, len(response.data))

    def test_can_read_a_specific_account(self):
        account = AccountFactory()

        response = self.client.get(reverse('accounts:account-detail', args=[account.id]))

        self.assertEquals(200, response.status_code)
        self.assertEquals(account.email, response.data['email'])
        self.assertEquals(str(account.id), response.data['id'])
        # Password should be hidden
        self.assertFalse('password' in response.data)

    def test_can_edit_an_account(self):
        account = AccountFactory()
        payload = {
            'email': 'new_email@example.com',
        }

        response = self.client.patch(reverse('accounts:account-detail', args=[account.id]), payload)
        account.refresh_from_db()

        self.assertEquals(200, response.status_code)
        self.assertEquals(payload['email'], response.data['email'])
        self.assertEquals(payload['email'], account.email)

    def test_password_cant_be_changed_directly(self):
        account = AccountFactory()
        old_password = account.password
        payload = {
            'email': account.email,
            'password': 'new_password'
        }

        response = self.client.patch(reverse('accounts:account-detail', args=[account.id]), payload)
        account.refresh_from_db()

        self.assertEquals(200, response.status_code)
        self.assertEquals(old_password, account.password)

    def test_can_create_a_new_account(self):
        payload = {
            'email': 'jdoe@example.com',
            'password1': 'p@ssw0rd!',
            'password2': 'p@ssw0rd!',
        }

        response = self.client.post(reverse('accounts:account-list'), payload)
        new_account = Account.objects.first()

        self.assertEquals(201, response.status_code)
        self.assertEquals(payload['email'], response.data['email'])
        self.assertEqual(payload['email'], new_account.email)
        self.assertTrue(new_account.password)
        # The password should be encrypted
        self.assertNotEquals(payload['password1'], new_account.password)

    def test_can_delete_an_account(self):
        account = AccountFactory()

        response = self.client.delete(reverse('accounts:account-detail', args=[account.id]))

        self.assertEquals(204, response.status_code)
        self.assertEquals(0, Account.objects.count())
