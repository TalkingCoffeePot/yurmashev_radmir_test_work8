from django.forms import forms
from products.models import Products, Review

class ProductForm(forms.Form):
    class Meta:
        model = Products
        fields = [
            'title',
            'category',
            'description',
            'image',
        ]

class ReviewForm(forms.Form):
    class Meta:
        model =Review
        fields = [
            'text',
            'rate',
        ]