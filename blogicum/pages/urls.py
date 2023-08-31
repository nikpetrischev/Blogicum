# Django Library
from django.urls import path
from django.views.generic.base import TemplateView

# Namespace - pages.
app_name = 'pages'

# List of info-pages' addresses.
urlpatterns = [
    path(
        'about/',
        TemplateView.as_view(template_name='pages/about.html'),
        name='about'
    ),
    path(
        'rules/',
        TemplateView.as_view(template_name='pages/rules.html'),
        name='rules'
    ),
]
