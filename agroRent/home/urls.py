from django.urls import path
from home.views import (
    BannerListView, PopularEquipmentListView, HomeContentDetailView, 
    TranslateView, SiteTextListView, SiteTextDetailView
)

urlpatterns = [
    path('banners/', BannerListView.as_view(), name='banner-list'),
    path('banners/<uuid:pk>/', HomeContentDetailView.as_view(), name='banner-detail'),
    path('popular-equipment/', PopularEquipmentListView.as_view(), name='popular-equipment-list'),
    path('translate/', TranslateView.as_view(), name='translate'),
    path('site-texts/', SiteTextListView.as_view(), name='sitetext-list'),
    path('site-texts/<int:pk>/', SiteTextDetailView.as_view(), name='sitetext-detail'),
]

