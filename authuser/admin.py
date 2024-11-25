from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'lastName', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name', 'lastName')
    actions = ['delete_selected']  # Make sure delete action is enabled

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset  # Ensure no filtering that might prevent access to the superuser

    def has_delete_permission(self, request, obj=None):
        # This allows superusers to delete other superusers
        if obj is not None and obj.is_superuser:
            return True
        return super().has_delete_permission(request, obj)