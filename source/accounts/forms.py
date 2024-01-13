from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) < 1:
            raise forms.ValidationError("Email обязателен к заполнению!")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data['first_name']) < 1 and len(cleaned_data['last_name']) < 1:
            raise forms.ValidationError("Хотя бы одно поле ИМЕНИ должно быть заполнено")
        return cleaned_data