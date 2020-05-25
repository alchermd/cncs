from datetime import datetime

from rest_framework.test import APITestCase

from snippets.tests.factories import SnippetFactory


class SnippetsModelTest(APITestCase):
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
