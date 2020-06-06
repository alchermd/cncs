import json
import random

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.helpers import generate_tokens
from accounts.tests.factories import AccountFactory, ApplicationFactory
from snippets.models import Snippet
from snippets.tests.factories import SnippetFactory


class SnippetViewsTest(APITestCase):
    def test_can_browse_all_snippets(self):
        snippets = SnippetFactory.create_batch(random.randint(1, 5))

        response = self.client.get(reverse('snippets:snippet-list'))

        self.assertEquals(len(snippets), len(response.data))

    def test_can_read_a_specific_snippet(self):
        snippet = SnippetFactory()

        response = self.client.get(reverse('snippets:snippet-detail', args=[snippet.key]))

        self.assertEquals(snippet.title, response.data['title'])
        self.assertEquals(snippet.code, response.data['code'])
        self.assertEquals(snippet.has_line_numbers, response.data['has_line_numbers'])

    def test_can_edit_a_specific_snippet(self):
        snippet = SnippetFactory(
            title='Hello, World!',
            code='print("hello, world!")',
            language='python',
        )

        payload = {
            'title': 'Hello, World! But in Ruby',
            'code': 'puts "hello, world!"',
            'language': 'rb',
        }
        response = self.client.patch(reverse('snippets:snippet-detail', args=[snippet.key]), payload)
        snippet.refresh_from_db()

        self.assertEquals(response.data['title'], payload['title'])
        self.assertEquals(response.data['code'], payload['code'])
        self.assertEquals(response.data['language'], payload['language'])

        self.assertEquals(snippet.title, payload['title'])
        self.assertEquals(snippet.code, payload['code'])
        self.assertEquals(snippet.language, payload['language'])

    def test_can_add_a_new_snippet(self):
        payload = {
            'title': 'My First C Program',
            'code': '#include <stdio.h>\nint main(){\nreturn 0;\n}',
            'language': 'c',
            'has_line_numbers': True,
        }

        response = self.client.post(reverse('snippets:snippet-list'), payload)
        snippet = Snippet.objects.first()

        self.assertEquals(response.data['title'], payload['title'])
        self.assertEquals(response.data['code'], payload['code'])
        self.assertEquals(response.data['language'], payload['language'])
        self.assertEquals(response.data['has_line_numbers'], payload['has_line_numbers'])

        self.assertEquals(snippet.title, payload['title'])
        self.assertEquals(snippet.code, payload['code'])
        self.assertEquals(snippet.language, payload['language'])
        self.assertEquals(snippet.has_line_numbers, payload['has_line_numbers'])

    def test_can_delete_a_snippet(self):
        snippet = SnippetFactory()

        self.client.delete(reverse('snippets:snippet-detail', args=[snippet.key]))

        self.assertEquals(Snippet.objects.count(), 0)

    def test_creating_a_snippet_while_logged_in_will_assign_the_user_as_the_snippets_owner(self):
        app = ApplicationFactory()
        account = AccountFactory()
        account.set_password('p@ssw0rd!')
        account.save()
        access_token, _ = generate_tokens(app, account)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + access_token.token
        }
        payload = {
            'title': 'My First C Program',
            'code': '#include <stdio.h>\nint main(){\nreturn 0;\n}',
            'language': 'c',
            'has_line_numbers': True,
        }

        response = self.client.post(reverse('snippets:snippet-list'), payload, **headers)
        snippet = Snippet.objects.first()

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(account, snippet.owner)

    def test_can_set_a_snippets_password(self):
        account = AccountFactory()
        app = ApplicationFactory()
        access_token, _ = generate_tokens(app, account)
        snippet = SnippetFactory(owner=account)
        headers = {
            'HTTP_AUTHORIZATION': f'Bearer {access_token.token}'
        }
        payload = {
            'password1': 'p@ssw0rd!',
            'password2': 'p@ssw0rd!',
        }

        response = self.client.post(reverse('snippets:snippet-set-password', args=[snippet.key]), json.dumps(payload),
                                    **headers,
                                    content_type='application/json')
        snippet.refresh_from_db()

        self.assertTrue(snippet.password)

        response = self.client.get(reverse('snippets:snippet-detail', args=[snippet.key]))
        self.assertEquals(status.HTTP_403_FORBIDDEN, response.status_code)

        response = self.client.get(reverse('snippets:snippet-detail', args=[snippet.key]), **headers)
        self.assertEquals(status.HTTP_200_OK, response.status_code)
