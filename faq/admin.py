from django.contrib import admin

from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'language')
    list_filter = ('language',)
    search_fields = ('question', 'answer')
    
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'language')
        }),
        ('Hindi Translation', {
            'fields': ('question_hi', 'answer_hi')
        }),
        ('Bengali Translation', {
            'fields': ('question_bn', 'answer_bn')
        }),
    )

# Register your models here.
