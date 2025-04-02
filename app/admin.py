from django.contrib import admin
from .models import Role, User, product_type, Product, OrderProduct, Status, Order
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Role modelini admin panelga qo'shish
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)

# User modelini admin panelga qo'shish
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'role', 'is_available')
    list_filter = ('role', 'is_available')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-id',)

    # Parolni avtomatik hash qilish
    def save_model(self, request, obj, form, change):
        if change and 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

# Product Type modelini admin panelga qo'shish
@admin.register(product_type)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)

# Product modelini admin panelga qo'shish
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price')
    list_filter = ('type',)
    search_fields = ('name', 'description')
    ordering = ('-id',)

# OrderProduct modelini admin panelga qo'shish
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'price_at_order', 'subtotal')
    search_fields = ('product__name',)
    ordering = ('-id',)

# Status modelini admin panelga qo'shish
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('-id',)

# Order modelini admin panelga qo'shish
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'status', 'order_time', 'total_price')
    list_filter = ('status',)
    search_fields = ('table_number',)
    ordering = ('-id',)
