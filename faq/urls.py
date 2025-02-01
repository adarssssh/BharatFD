# from django.urls import path
# from .views import FAQView, faq_detail

# urlpatterns = [
#     path('faqs/', FAQView.as_view({'get': 'list'}), name='faq-list'),
#     path('faqs/<int:pk>/', FAQView.as_view({'get': 'retrieve'}), name='faq-detail'),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FAQView

router = DefaultRouter()
router.register(r'faqs', FAQView, basename='faq')

urlpatterns = [
    path('api/', include(router.urls)),  # Ensure ViewSet is included
]