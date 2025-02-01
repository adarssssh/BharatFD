from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.response import Response



from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQView(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def list(self, request):
        """Retrieve all FAQs in a specific language with caching."""
        language = request.query_params.get('lang', 'en')
        cache_key = f'faqs_{language}'

        cached_faqs = cache.get(cache_key)
        if cached_faqs:
            return Response(cached_faqs)

        faqs = self.get_queryset()
        faq_data = [
            {
                'faq_id': faq.id,
                'question': faq.get_translated_question(language),
                'answer': faq.get_translated_answer(language)
            }
            for faq in faqs
        ]

        cache.set(cache_key, faq_data, timeout=100)  # Cache for 1 minute
        return Response(faq_data)

    def retrieve(self, request, pk=None):
        """Retrieve a single FAQ with caching and language support."""
        language = request.query_params.get('lang', 'en')
        cache_key = f'faq_{pk}_{language}'

        cached_faq = cache.get(cache_key)
        if cached_faq:
            return Response(cached_faq)

        faq = get_object_or_404(FAQ, pk=pk)

        faq_data = {
            'faq_id': faq.id,
            'question': faq.get_translated_question(language),
            'answer': faq.get_translated_answer(language)
        }

        cache.set(cache_key, faq_data, timeout=100)  # Cache for 1 hour
        return Response(faq_data)

    def perform_update(self, serializer):
        """Invalidate cache when an FAQ is updated."""
        instance = serializer.save()
        self._invalidate_cache(instance.id)

    def perform_destroy(self, instance):
        """Invalidate cache when an FAQ is deleted."""
        self._invalidate_cache(instance.id)
        instance.delete()

    def _invalidate_cache(self, faq_id):
        """Helper function to remove all cached translations for a specific FAQ."""
        languages = ['en', 'hi', 'bn']  # Add more if needed
        keys_to_delete = [f'faq_{faq_id}_{lang}' for lang in languages]
        keys_to_delete += [f'faqs_{lang}' for lang in languages]  # Invalidate all FAQ lists
        
        for key in keys_to_delete:
            cache.delete(key)







