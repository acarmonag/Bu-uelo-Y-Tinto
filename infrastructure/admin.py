from django.contrib import admin
from infrastructure.models.user import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('username',)
    
    # Acciones personalizadas del src/admin.py
    actions = ['delete_selected', 'activate_selected', 'inactivate_selected']
    
    def delete_selected(self, request, queryset):
        queryset.update(deleted=True)
    delete_selected.short_description = 'Eliminar seleccionados'
    
    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
    activate_selected.short_description = 'Activar seleccionados'
    
    def inactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
    inactivate_selected.short_description = 'Inactivar seleccionados' 