from django.urls import path
from market.views import (
    CategoryListView, CategoryDetailView, MarketItemListView, MarketItemCreateView,
    MarketItemDetailView, MarketOrderCreateView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('items/', MarketItemListView.as_view(), name='market-item-list'),
    path('items/create/', MarketItemCreateView.as_view(), name='market-item-create'),
    path('items/<uuid:pk>/', MarketItemDetailView.as_view(), name='market-item-detail'),
    path('orders/create/', MarketOrderCreateView.as_view(), name='market-order-create'),
]
