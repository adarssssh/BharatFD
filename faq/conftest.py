import os
import django
from django.conf import settings

# Configure Django settings for pytest
def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faq_project.settings')
    settings.DEBUG = True
    django.setup()