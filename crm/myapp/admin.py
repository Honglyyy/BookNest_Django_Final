from django.contrib import admin

from myapp.models import Product, Category, ProductDetailImage, ProductDetail, Blog, Genre, BillingDetail

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductDetailImage)
admin.site.register(Blog)
admin.site.register(Genre)
admin.site.register(BillingDetail)
