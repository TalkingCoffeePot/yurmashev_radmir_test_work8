from django.forms import ModelForm, TextInput, RadioSelect, Textarea
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
    RATE = [1, 2, 3, 4, 5]
    class Meta:
        model = Review
        fields = [
            'author',
            'product',
            'text',
            'rate',
            'moderate'
        ]
        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Оставьте комментарий'
            }),
            'rate': RadioSelect(attrs={
                'class': 'btn btn-primary'
            })
        }

