from django.contrib import admin

from .models import Order, OrderItem


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "ordered_by", "status", "paid", "dispatched", "coupon", "created", "updated",
                    "delivery_method", "total_cost_with_shipping_with_discount"]
    list_filter = ["status", "coupon", "created", "delivery_method", "dispatched"]
    inlines = [OrderItemInline]
    search_fields = ["order_number"]
