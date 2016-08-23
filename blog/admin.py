from django.contrib import admin

from .models import Blog, Product

class BlogAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Product, ProductAdmin)
