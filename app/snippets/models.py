import random
import string

from django.contrib.auth.hashers import make_password
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

from accounts.models import Account
from commons.models import TimestampedModel

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


def generate_key(length):
    characters = []
    for _ in range(length):
        random_character = random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        characters.append(random_character)
    return ''.join(characters)


class Snippet(TimestampedModel):
    key = models.CharField(max_length=4, primary_key=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    has_line_numbers = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(
        choices=STYLE_CHOICES, default='friendly', max_length=100)
    highlighted = models.TextField()
    password = models.CharField(max_length=128, null=True)
    owner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        # Use the `pygments` library to create a highlighted HTML representation of the code snippet.
        lexer = get_lexer_by_name(self.language)
        has_line_numbers = self.has_line_numbers and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(
            style=self.style, linenos=has_line_numbers, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

        # Generate a unique key upon insertion.
        if self.key == '':
            while key := generate_key(4):
                try:
                    Snippet.objects.get(key=key)
                    continue
                except Snippet.DoesNotExist:
                    self.key = key
                    break

        super(Snippet, self).save(*args, **kwargs)

    def set_password(self, password):
        self.password = make_password(password)
        self.save()
        return self
