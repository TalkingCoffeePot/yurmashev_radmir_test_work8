from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.contrib.auth.models import User
from accounts.forms import NewUserForm
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
    return redirect('products')

class UserRegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('products'))
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('products')
        return next_url