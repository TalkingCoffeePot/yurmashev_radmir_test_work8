from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import NewUserForm, UserEditForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
# Create your views here.

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('products')
        else:
            context['has_error'] = True

    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('product_list')

class UserRegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('product_list'))
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('products_list')
        return next_url
    
class UserProfile(ListView):
    template_name = 'accounts/profile.html'
    model = User

class UserProfileEdit(UpdateView):
    model = User
    template_name = 'accounts/profile_edit.html'
    pk_url_kwarg = 'user_pk'
    form_class = UserEditForm
    #permission_required = 'main_app.change_projects'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'user_pk': self.object.pk})