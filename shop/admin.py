from django.contrib import admin

from .models import Product, ProductCategory, ProductColour, ProductImage


# Register your models here.
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", ]
    prepopulated_fields = {"slug": ("name", )}


class ProductImageInline(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "category", "price", "stock", "available", "date_created",]
    list_filter = ["category", "available", "date_created"]
    list_editable = ["available", "price"]
    prepopulated_fields = {"slug": ("name", )}
    inlines = [ProductImageInline]
    search_fields = ["name", "price"]


@admin.register(ProductColour)
class ProductColourAdmin(admin.ModelAdmin):
    pass
