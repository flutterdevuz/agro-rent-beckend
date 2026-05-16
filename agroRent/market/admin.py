from django.contrib import admin
from market.models import Category, MarketItem, MarketOrder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(MarketItem)
class MarketItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'seller', 'created_at')
    list_filter = ('category', 'condition', 'has_delivery')
    search_fields = ('name', 'brand', 'model', 'description')

@admin.register(MarketOrder)
class MarketOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user', 'quantity', 'delivery_date', 'created_at')
    list_filter = ('delivery_date', 'created_at')
    search_fields = ('user__phone_number', 'item__name')
