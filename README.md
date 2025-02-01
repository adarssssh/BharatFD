# BharatFD
Hiring assignment

FAQ Management System with Multilingual Support

A Django-based FAQ management system that allows for rich text formatting of answers, supports multiple languages (e.g., English, Hindi, Bengali), and provides an API to retrieve FAQs with language-specific translations.


Features:

    FAQ Management: Store questions, answers, and translations for multiple languages.
    Multilingual Support: Supports English, Hindi, and Bengali translations.
    REST API: Provides an API to retrieve FAQs with language selection via query parameters.
    Caching: Redis caching mechanism for optimized performance.
    Admin Interface: An intuitive admin panel for managing FAQs and their translations.

Steps to run:

1.Cloning:
 git clone https://github.com/adarssssh/BharatFD.git
2. Install virtual env :
  python -m venv venv
  source venv/bin/activate
3.Installing dependencies:
  pip install -r requirements.txt
4. Database setup:
  python manage.py makemigrations
  python manage.py migrate
5. Run the application:
  python manage.py runserver


API Usage:

1. Get all FAQs: /api/faqs/
2. Get all FAQs based on Language: /api/faqs/?lang=hi
3. Get individual FAQ using FAQ_id: /api/faqs/1 
4. Get individual FAQ in languages: /api/faqs/1/?lang=hi

Update Faqs using Admin dashboard.
Caching applied for 1 minute.







