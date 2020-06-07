from datetime import datetime

from django.test import TestCase

from accounts.tests.factories import AccountFactory
from snippets.models import Snippet
from snippets.tests.factories import SnippetFactory


class SnippetsModelTest(TestCase):
    def setUp(self):
        self.snippet = SnippetFactory()

    def test_it_has_timestamp_fields(self):
        self.assertTrue(hasattr(self.snippet, 'created_at'))
        self.assertTrue(hasattr(self.snippet, 'updated_at'))

        self.assertIsInstance(self.snippet.created_at, datetime)
        self.assertIsInstance(self.snippet.updated_at, datetime)

    def test_it_has_code_related_fields(self):
        self.assertTrue(hasattr(self.snippet, 'title'))
        self.assertTrue(hasattr(self.snippet, 'code'))
        self.assertTrue(hasattr(self.snippet, 'has_line_numbers'))
        self.assertTrue(hasattr(self.snippet, 'language'))
        self.assertTrue(hasattr(self.snippet, 'style'))
        self.assertTrue(hasattr(self.snippet, 'highlighted'))

        self.assertIsInstance(self.snippet.title, str)
        self.assertIsInstance(self.snippet.code, str)
        self.assertIsInstance(self.snippet.has_line_numbers, bool)
        self.assertIsInstance(self.snippet.language, str)
        self.assertIsInstance(self.snippet.style, str)
        self.assertIsInstance(self.snippet.highlighted, str)

    def test_it_has_an_alternative_primary_key(self):
        self.assertTrue(hasattr(self.snippet, 'key'))
        self.assertIsInstance(self.snippet.key, str)
        self.assertEquals(4, len(self.snippet.key))

    def test_it_can_have_an_owner(self):
        self.assertTrue(hasattr(self.snippet, 'owner'))
        self.assertIsNone(self.snippet.owner)

        account = AccountFactory()
        self.snippet.owner = account
        self.snippet.save()

        snippet = Snippet.objects.get(pk=self.snippet.key)
        self.assertEquals(snippet.owner, account)

    def test_it_can_have_a_password(self):
        account = AccountFactory()
        self.snippet.owner = account
        self.snippet.save()

        self.snippet.set_password('p@ssw0rd!')
        snippet = Snippet.objects.get(pk=self.snippet.key)

        self.assertIsNotNone(snippet.password)
        self.assertNotEquals('p@ssw0rd!', snippet.password)
