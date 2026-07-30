from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('faq/', views.faq, name='faq'),
    path('lead-tool/', views.lead_tool, name='lead_tool'),
    path('guide/', views.guide, name='guide'),
    path('crm/', views.crm, name='crm'),
]
