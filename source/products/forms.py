from django.forms import ModelForm
from products.models import Products, Review

class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = [
            'title',
            'category',
            'description',
            'image',
        ]

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'author',
            'product',
            'text',
            'rate',
        ]
