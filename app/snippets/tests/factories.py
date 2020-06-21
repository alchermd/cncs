import random
from datetime import datetime

import factory

from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetFactory(factory.DjangoModelFactory):
    class Meta:
        model = Snippet

    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    title = factory.Faker('sentence')
    code = factory.Faker('paragraph').generate()
    has_line_numbers = factory.Faker('boolean')
    language = random.choice(LANGUAGE_CHOICES)[0]
    style = random.choice(STYLE_CHOICES)[0]
