from django.contrib import admin

from products.models import Product, ProductImages, ProductSpecifications, Specification

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(ProductSpecifications)
admin.site.register(Specification)
