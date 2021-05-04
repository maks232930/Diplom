from django.contrib import admin

from shop.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'price', 'is_published',)
    list_display_links = ('name', 'quantity', 'price',)
    list_editable = ('is_published',)


admin.site.register(Product, ProductAdmin)
