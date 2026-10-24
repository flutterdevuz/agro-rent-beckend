from django.urls import path
from home.views import (
    BannerListView, PopularEquipmentListView, HomeContentDetailView, 
    TranslateView, SiteTextListView, SiteTextDetailView,
    WebsiteContentAPIView, WebsiteOrderCreateView,
    AdminWebsiteSettingsView, AdminWebsiteServiceListCreateView,
    AdminWebsiteServiceDetailView, AdminWebsitePartnerListCreateView,
    AdminWebsitePartnerDetailView, AdminWebsiteOrderListView,
    AdminWebsiteOrderDetailView,
    AdminWebsiteStepListCreateView, AdminWebsiteStepDetailView,
    AdminWebsiteBenefitListCreateView, AdminWebsiteBenefitDetailView
)

urlpatterns = [
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('banners/<uuid:pk>/', HomeContentDetailView.as_view(), name='banner-detail'),
    path('popular-equipment/', PopularEquipmentListView.as_view(), name='popular-equipment-list'),
    path('translate/', TranslateView.as_view(), name='translate'),
    path('site-texts/', SiteTextListView.as_view(), name='sitetext-list'),
    path('site-texts/<int:pk>/', SiteTextDetailView.as_view(), name='sitetext-detail'),

    # Website Public APIs
    path('website/content/', WebsiteContentAPIView.as_view(), name='website-content'),
    path('website/orders/', WebsiteOrderCreateView.as_view(), name='website-order-create'),

    # Website Admin APIs
    path('website/admin/settings/', AdminWebsiteSettingsView.as_view(), name='admin-website-settings'),
    path('website/admin/services/', AdminWebsiteServiceListCreateView.as_view(), name='admin-website-services'),
    path('website/admin/services/<int:pk>/', AdminWebsiteServiceDetailView.as_view(), name='admin-website-service-detail'),
    path('website/admin/partners/', AdminWebsitePartnerListCreateView.as_view(), name='admin-website-partners'),
    path('website/admin/partners/<int:pk>/', AdminWebsitePartnerDetailView.as_view(), name='admin-website-partner-detail'),
    path('website/admin/orders/', AdminWebsiteOrderListView.as_view(), name='admin-website-orders-list'),
    path('website/admin/orders/<int:pk>/', AdminWebsiteOrderDetailView.as_view(), name='admin-website-order-detail'),
    path('website/admin/steps/', AdminWebsiteStepListCreateView.as_view(), name='admin-website-steps'),
    path('website/admin/steps/<int:pk>/', AdminWebsiteStepDetailView.as_view(), name='admin-website-step-detail'),
    path('website/admin/benefits/', AdminWebsiteBenefitListCreateView.as_view(), name='admin-website-benefits'),
    path('website/admin/benefits/<int:pk>/', AdminWebsiteBenefitDetailView.as_view(), name='admin-website-benefit-detail'),
]
