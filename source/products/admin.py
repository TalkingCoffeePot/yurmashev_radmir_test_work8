from django.contrib import admin
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
        'author.username',
        'product.title',
        'text',
        'rate',
        'moderate',
        'date_add',
        'date_edit',
    ]
