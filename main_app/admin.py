from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Wishlist
# ------------------------
# CATEGORY ADMIN
# ------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


# ------------------------
# PRODUCT ADMIN
# ------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available')
    list_filter = ('category', 'is_available')
    list_editable = ('price', 'stock', 'is_available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')
    ordering = ('-created_at',)


# ------------------------
# CART ADMIN
# ------------------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]
    search_fields = ('user__username',)


# ------------------------
# ORDER ADMIN
# ------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'id')
    inlines = [OrderItemInline]
    ordering = ('-order_date',)


# ------------------------
# WISHLIST ADMIN
# ------------------------
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('created_at',)
