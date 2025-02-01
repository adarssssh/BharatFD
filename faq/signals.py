from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FAQ
from django.core.cache import cache

# Signal handler to update the cache after saving the FAQ record
@receiver(post_save, sender=FAQ)
def update_faq_cache(sender, instance, created, **kwargs):
    # Cache the translations after saving or updating
    instance._cache_translations()

# Signal handler to clear the cache after deleting the FAQ record
@receiver(post_delete, sender=FAQ)
def delete_faq_cache(sender, instance, **kwargs):
    # Clear the cache for the deleted FAQ record
    cache.delete(f'faq_question_hi_{instance.pk}')
    cache.delete(f'faq_question_bn_{instance.pk}')
    cache.delete(f'faq_answer_hi_{instance.pk}')
    cache.delete(f'faq_answer_bn_{instance.pk}')
