from django.contrib import admin
from home.models import HomeContent

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'price')
    list_filter = ('content_type',)
    search_fields = ('name', 'description')
