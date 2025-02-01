from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from googletrans import Translator
import asyncio

LANGUAGES = [
    ('en', _('English')),
    ('hi', _('Hindi')),
    ('bn', _('Bengali')),
]

class FAQ(models.Model):
    question = models.TextField(verbose_name=_('Question'))
    answer = RichTextField(verbose_name=_('Answer'))
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')

    # Multilingual fields
    question_hi = models.TextField(verbose_name=_('Question in Hindi'), blank=True, null=True)
    question_bn = models.TextField(verbose_name=_('Question in Bengali'), blank=True, null=True)
    answer_hi = RichTextField(verbose_name=_('Answer in Hindi'), blank=True, null=True)
    answer_bn = RichTextField(verbose_name=_('Answer in Bengali'), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Prevent overwriting existing translations for new instances
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._translate_fields())

        super().save(*args, **kwargs)  # Save the record to the DB

        # After saving, cache the translated fields
        self._cache_translations()

    async def _translate_fields(self):
        if not self.question_hi and self.language != 'hi':
            self.question_hi = await self._translate(self.question, 'hi')

        if not self.question_bn and self.language != 'bn':
            self.question_bn = await self._translate(self.question, 'bn')

        if not self.answer_hi and self.language != 'hi':
            self.answer_hi = await self._translate(self.answer, 'hi')

        if not self.answer_bn and self.language != 'bn':
            self.answer_bn = await self._translate(self.answer, 'bn')

    async def _translate(self, text, target_lang):
        translator = Translator()
        cache_key = f'translation_{text}_{target_lang}'
        cached_translation = cache.get(cache_key)

        if cached_translation:
            return cached_translation

        try:
            translation = await translator.translate(text, dest=target_lang)
            cache.set(cache_key, translation.text, timeout=100)  # Cache for 1 hour
            return translation.text
        except Exception:
            return text  

    def _cache_translations(self):
        """Cache the translated fields."""
        if self.question_hi:
            cache.set(f'faq_question_hi_{self.pk}', self.question_hi, timeout=3600)
        if self.question_bn:
            cache.set(f'faq_question_bn_{self.pk}', self.question_bn, timeout=3600)
        if self.answer_hi:
            cache.set(f'faq_answer_hi_{self.pk}', self.answer_hi, timeout=3600)
        if self.answer_bn:
            cache.set(f'faq_answer_bn_{self.pk}', self.answer_bn, timeout=3600)

    def get_translated_question(self, lang='en'):
        translations = {
            'en': self.question,
            'hi': self.question_hi or self.question,
            'bn': self.question_bn or self.question
        }
        return translations.get(lang, self.question)

    def get_translated_answer(self, lang='en'):
        translations = {
            'en': self.answer,
            'hi': self.answer_hi or self.answer,
            'bn': self.answer_bn or self.answer
        }
        return translations.get(lang, self.answer)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
