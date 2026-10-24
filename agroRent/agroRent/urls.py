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
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users.permissions import SuperAdminOnly
from home.views import PublicHomeView, PublicMarketView, PublicRentView, PublicAboutView, PublicProfileView, PublicRentDetailView, handle_404

import hmac

from django.http import Http404

def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')

        # 1. Email va Auth tekshiruvi (staff, superuser yoki ruxsat etilgan email)
        is_allowed = request.user.is_superuser or request.user.is_staff or (request.user.email in SuperAdminOnly.ALLOWED_EMAILS)
        
        # 2. Access Key tekshiruvi
        if settings.ADMIN_ACCESS_KEY:
            access_key = request.GET.get('access')
            if access_key and hmac.compare_digest(access_key, settings.ADMIN_ACCESS_KEY):
                request.session['admin_access_verified'] = True
            is_access_verified = request.session.get('admin_access_verified', False)
        else:
            is_access_verified = True

        if is_allowed and is_access_verified:
            return view_func(request, *args, **kwargs)
        
        raise Http404()
    return wrapper

handler404 = handle_404

urlpatterns = [
    path('', PublicHomeView.as_view(), name='home'),
    path('market/', PublicMarketView.as_view(), name='market'),
    path('rent/', PublicRentView.as_view(), name='rent'),
    path('rent/<uuid:pk>/', PublicRentDetailView.as_view(), name='rent-detail'),
    path('about/', PublicAboutView.as_view(), name='about'),
    path('profile/', PublicProfileView.as_view(), name='profile'),
    path('django-admin/', admin.site.urls),
    path('admin/', superadmin_required(TemplateView.as_view(template_name='index.html')), name='custom-admin'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('forgot-password/', TemplateView.as_view(template_name='forgot-password.html'), name='forgot-password'),
    path('api/admin/banners/', superadmin_required(TemplateView.as_view(template_name='banners.html')), name='admin-banners'),
    path('api/admin/rent/', superadmin_required(TemplateView.as_view(template_name='rent.html')), name='admin-rent'),
    path('api/admin/market/', superadmin_required(TemplateView.as_view(template_name='market.html')), name='admin-market'),
    path('api/admin/categories/', superadmin_required(TemplateView.as_view(template_name='categories.html')), name='admin-categories'),
    path('api/admin/notifications/', superadmin_required(TemplateView.as_view(template_name='notifications.html')), name='admin-notifications'),
    path('api/admin/users/', superadmin_required(TemplateView.as_view(template_name='users.html')), name='admin-users'),
    path('api/admin/site-texts/', superadmin_required(TemplateView.as_view(template_name='site_texts.html')), name='admin-site-texts'),
    path('api/admin/website/', superadmin_required(TemplateView.as_view(template_name='website.html')), name='admin-website'),
    path('api/admin/website-orders/', superadmin_required(TemplateView.as_view(template_name='website_orders.html')), name='admin-website-orders-page'),
    # Restricted Documentation
    path('api/schema/', superadmin_required(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/', superadmin_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    path('api/redoc/', superadmin_required(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
    
    path('api/admin/banners/', superadmin_required(TemplateView.as_view(template_name='banners.html')), name='admin-banners'),
    path('api/admin/rent/', superadmin_required(TemplateView.as_view(template_name='rent.html')), name='admin-rent'),
    path('api/admin/market/', superadmin_required(TemplateView.as_view(template_name='market.html')), name='admin-market'),
    path('api/admin/categories/', superadmin_required(TemplateView.as_view(template_name='categories.html')), name='admin-categories'),
    path('api/admin/notifications/', superadmin_required(TemplateView.as_view(template_name='notifications.html')), name='admin-notifications'),
    path('api/admin/users/', superadmin_required(TemplateView.as_view(template_name='users.html')), name='admin-users'),
    
    path('api/users/', include('users.urls')),
    path('api/', include('home.urls')),
    path('api/rent/', include('rent.urls')),
    path('api/market/', include('market.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
