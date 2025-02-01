import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from .models import FAQ

@pytest.mark.django_db
class TestFAQModel(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question='What is Django?',
            answer='Django is a Python web framework.',
            language='en'
        )

    def test_model_creation(self):
        assert self.faq is not None
        assert self.faq.question == 'What is Django?'

    def test_translation_generation(self):
        # Check if translations are generated
        assert self.faq.question_hi is not None
        assert self.faq.answer_hi is not None

    def test_translation_retrieval(self):
        hi_question = self.faq.get_translated_question('hi')
        assert hi_question is not None
