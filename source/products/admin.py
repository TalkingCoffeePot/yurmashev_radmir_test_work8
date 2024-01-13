from django.contrib import admin
from django.contrib.auth.models import User
from products.models import Products, Review
# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'description',
        'image',
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'get_author',
        'product',
        'text',
        'rate',
        'moderate',
        'date_add',
        'date_edit',
    ]
    @admin.display(ordering='author__username')
    def get_author(self, obj):
        return User.objects.get(username=obj.author).id
    @admin.display(ordering='product__title')
    def get_product(self, obj):
        return Products.objects.get(id=obj.product).title
    