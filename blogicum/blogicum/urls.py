# Django Library
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf.urls.static import static
from django.views.generic import CreateView

from blog.forms import UserCreateForm


# List of pages' addresses.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreateForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
]

# List of custom handlers
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
