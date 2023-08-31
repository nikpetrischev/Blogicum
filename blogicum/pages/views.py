# Django Library
from django.shortcuts import render


# 403 error view
def permission_denied(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


# 404 error view
def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


# 500 error view
def server_error(request):
    return render(request, 'pages/500.html', status=500)
