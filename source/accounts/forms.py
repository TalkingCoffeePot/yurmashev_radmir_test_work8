from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
    
class UserEditForm(UserChangeForm):
    class Meta:
        model= User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['password', 'password_confirm', 'old_password']