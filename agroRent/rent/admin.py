from django.contrib import admin
from rent.models import RentItem, RentImage, RentOrder

class RentImageInline(admin.TabularInline):
    model = RentImage
    extra = 1

@admin.register(RentItem)
class RentItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment_name', 'owner', 'price', 'region', 'created_at')
    list_filter = ('region', 'condition', 'is_agreement')
    search_fields = ('name', 'equipment_name', 'brand')
    inlines = [RentImageInline]

@admin.register(RentOrder)
class RentOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'rent_item', 'user', 'order_date', 'created_at')
    list_filter = ('order_date', 'created_at')
    search_fields = ('user__phone_number', 'rent_item__equipment_name')
