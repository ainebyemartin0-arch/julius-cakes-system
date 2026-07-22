from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Category, Product, Order, OrderItem

# 1. Remove "Groups" to declutter the admin panel
admin.site.unregister(Group)

# 2. Inline display for Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_price',)

# 3. Order Admin (Moved to top so it's the first thing Julius sees)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'required_date', 'status', 'delivery_option', 'total_price')
    list_filter = ('status', 'delivery_option', 'required_date')
    search_fields = ('customer_name', 'customer_phone', 'id')
    readonly_fields = ('created_at', 'cake_details')
    inlines = [OrderItemInline]
    ordering = ('-created_at',) # Newest orders at the top
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Order Details', {
            'fields': ('cake_details', 'reference_image', 'total_price', 'status')
        }),
        ('Fulfillment', {
            'fields': ('delivery_option', 'delivery_address', 'required_date', 'created_at')
        }),
    )

# 4. Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'is_custom')
    list_filter = ('category', 'is_custom')
    search_fields = ('name', 'description')

# 5. Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Remove the buggy unregister line from before
admin.site.unregister(Order) if Order in admin.site._registry else None
admin.site.register(Order, OrderAdmin)

# Custom Admin Site Headers (Re-applied to be safe)
admin.site.site_header = "Julius Cakes Control Center"
admin.site.site_title = "Julius Cakes Admin"
admin.site.index_title = "Bakery Management"
