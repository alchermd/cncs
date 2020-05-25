import random
from datetime import datetime

import factory

from snippets.models import Snippet


class SnippetFactory(factory.Factory):
    class Meta:
        model = Snippet

    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
    title = factory.Faker('sentence')
    code = factory.Faker('paragraph').generate()
    has_line_numbers = factory.Faker('boolean')
    language = random.choice(Snippet.LANGUAGE_CHOICES)[0]
    style = random.choice(Snippet.STYLE_CHOICES)[0]
