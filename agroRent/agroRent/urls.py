"""
URL configuration for agroRent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.views.generic import TemplateView
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', TemplateView.as_view(template_name='index.html'), name='custom-admin'),
    path('api/admin/login/', TemplateView.as_view(template_name='login.html'), name='admin-login'),
    path('api/admin/banners/', TemplateView.as_view(template_name='banners.html'), name='admin-banners'),
    path('api/admin/rent/', TemplateView.as_view(template_name='rent.html'), name='admin-rent'),
    path('api/admin/market/', TemplateView.as_view(template_name='market.html'), name='admin-market'),
    path('api/admin/categories/', TemplateView.as_view(template_name='categories.html'), name='admin-categories'),
    path('api/admin/notifications/', TemplateView.as_view(template_name='notifications.html'), name='admin-notifications'),
    path('api/admin/users/', TemplateView.as_view(template_name='users.html'), name='admin-users'),
    path('api/users/', include('users.urls')),
    path('api/', include('home.urls')),
    path('api/rent/', include('rent.urls')),
    path('api/market/', include('market.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # Swagger UI:
    path('api/schema/', SpectacularAPIView.as_view(
        permission_classes=[IsAdminUser],
        authentication_classes=[BasicAuthentication]
    ), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(
        url_name='schema',
        permission_classes=[IsAdminUser],
        authentication_classes=[BasicAuthentication]
    ), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(
        url_name='schema',
        permission_classes=[IsAdminUser],
        authentication_classes=[BasicAuthentication]
    ), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
