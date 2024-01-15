from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group
from accounts.forms import NewUserForm, UserEditForm, PasswordChangeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from products.models import Review
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from products.forms import ReviewForm
from django.contrib.auth import get_user_model
from typing import Any
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
        group = Group.objects.get(name='Пользователь')
        user.groups.add(group)
        login(self.request, user)
        return redirect(reverse('product_list'))
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('products_list')
        return next_url
    
class UserProfile(DetailView):
    template_name = 'accounts/profile.html'
    model = User
    context_object_name = 'user_obj'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        print(kwargs) 
        return super().get_context_data(**kwargs)

class UserProfileEdit(UpdateView):
    model = User
    template_name = 'accounts/profile_edit.html'
    pk_url_kwarg = 'user_pk'
    context_object_name = 'user_obj'
    form_class = UserEditForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        kwargs['user_obj'] = self.get_object()
        print(kwargs)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'user_pk': self.object.pk})
    
class ReviewEdit(PermissionRequiredMixin, UpdateView):
    
    model = Review
    template_name = 'products/review_edit.html'
    pk_url_kwarg = 'review_pk'
    form_class = ReviewForm
    context_object_name = 'review'
    permission_required = 'products.edit_rev'

    def get_success_url(self, **kwargs):
        return reverse('accounts:profile', kwargs={'user_pk': self.request.user.pk})
    
    def get_context_data(self, **kwargs):
        kwargs['review'] = self.get_object()
        kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)
    
    
class ModerateReviewEdit(PermissionRequiredMixin, UpdateView):
    
    model = Review
    template_name = 'products/review_edit.html'
    pk_url_kwarg = 'review_pk'
    form_class = ReviewForm
    context_object_name = 'review'
    permission_required = 'products.edit_rev'

    def get_context_data(self, **kwargs):
        kwargs['review'] = self.get_object()
        kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)
    
    def get_success_url(self):
        return reverse_lazy('moderation')
    
class ReviewDelete( PermissionRequiredMixin, DeleteView):
    
    model = Review
    template_name = 'products/delete.html'
    pk_url_kwarg = 'review_pk'
    context_object_name = 'review'
    this_author = ''
    this_product = ''
    permission_required = 'products.delete_rev'
    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('accounts:profile', kwargs={'user_pk': self.kwargs.get('user_pk')})
    
class ModerateReviewDelete(PermissionRequiredMixin, DeleteView):
    
    model = Review
    template_name = 'products/delete.html'
    pk_url_kwarg = 'review_pk'
    context_object_name = 'review'
    permission_required = 'products.delete_rev'

    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('moderation')
    
class UserPasswordChangeView(PermissionRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/pass_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user'
    pk_url_kwarg = 'user_pk'

    def get_success_url(self):
        return reverse('accounts:login')