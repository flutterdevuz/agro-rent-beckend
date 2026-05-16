from django.urls import path
from rent.views import (
    RentItemListView, RentItemCreateView, 
    RentItemDetailView, RentOrderCreateView,
    RentItemMeView
)

urlpatterns = [
    path('me/', RentItemMeView.as_view(), name='rent-item-me'),
    path('items/', RentItemListView.as_view(), name='rent-item-list'),
    path('items/create/', RentItemCreateView.as_view(), name='rent-item-create'),
    path('items/<uuid:pk>/', RentItemDetailView.as_view(), name='rent-item-detail'),
    path('orders/create/', RentOrderCreateView.as_view(), name='rent-order-create'),
]
