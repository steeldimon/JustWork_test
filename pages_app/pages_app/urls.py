from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/', include('api_app.urls')),
    path('', RedirectView.as_view(url='admin/', permanent=False), name='index')
]
