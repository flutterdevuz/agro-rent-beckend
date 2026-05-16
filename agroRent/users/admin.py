from django.contrib import admin
from users.models import User, ResetPasswordRequest

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'region', 'district')
    search_fields = ('phone_number', 'first_name', 'last_name')

@admin.register(ResetPasswordRequest)
class ResetPasswordRequestAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'description', 'created_at', 'is_resolved')
    list_filter = ('is_resolved',)
    search_fields = ('phone_number',)
