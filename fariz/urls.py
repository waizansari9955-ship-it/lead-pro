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
    path('scraper/', views.scraper, name='scraper'),
    path('api/live-scrape/', views.api_live_scrape, name='api_live_scrape'),
    path('api/live-search-leads/', views.api_live_search_leads, name='api_live_search_leads'),
]


