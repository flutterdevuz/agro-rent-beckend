from django.contrib import admin
from home.models import (
    HomeContent, WebsiteSettings, WebsiteService, WebsitePartner,
    WebsiteStep, WebsiteBenefit, WebsiteOrder
)

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'price')
    list_filter = ('content_type',)
    search_fields = ('name', 'description')

@admin.register(WebsiteSettings)
class WebsiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hero_title', 'phone_number', 'updated_at')

@admin.register(WebsiteService)
class WebsiteServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'price_estimate', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'slug', 'description')

@admin.register(WebsitePartner)
class WebsitePartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'member_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('member_type', 'is_active')
    search_fields = ('name', 'role')

@admin.register(WebsiteStep)
class WebsiteStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')
    list_editable = ('order',)

@admin.register(WebsiteBenefit)
class WebsiteBenefitAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)

@admin.register(WebsiteOrder)
class WebsiteOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'created_at', 'is_contacted')
    list_filter = ('is_contacted', 'service', 'created_at')
    list_editable = ('is_contacted',)
    search_fields = ('name', 'phone', 'message', 'admin_notes')
