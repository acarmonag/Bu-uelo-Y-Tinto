from django.contrib import admin
from infrastructure.models.user import User
from infrastructure.models.product import Product
from infrastructure.models.order import Order, OrderDetail
from infrastructure.models.order_status import OrderStatus

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    search_fields = ('name', 'price')
    list_filter = ['is_active']
    ordering = ('name',)
    
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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__username', 'delivery_location')
    
    # Acciones personalizadas
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

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ['is_active']
    ordering = ('name',)
    
    # Acciones personalizadas
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

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name') 