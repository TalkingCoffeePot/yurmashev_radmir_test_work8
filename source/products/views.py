from typing import Any
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from products.models import Products, Review
from django.contrib import auth
from django.shortcuts import get_object_or_404
from products.forms import ProductForm, ReviewForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.

class ProductListView(ListView):
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    model = Products

class ProductDetailedView(FormMixin, DetailView):
    
    template_name = 'products/product_detailed.html'
    model = Products
    form_class = ReviewForm
    context_object_name = 'product'
    pk_url_kwarg = 'product_pk'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context

    def get_success_url(self, **kwargs) -> str:
        return reverse_lazy('detailed_product', kwargs={'product_pk': self.get_object().id})
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(kwargs)
        if form.is_valid():
            return self.form_valid(form)
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.product = self.get_object()
        self.object.save()
        return super().form_valid(form)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    
    template_name = 'products/product_create.html'
    form_class = ProductForm
    permission_required = 'products.create_prod'

    def get_success_url(self):
        return reverse('product_list')
    
class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    
    model = Products
    template_name = 'products/product_update.html'
    pk_url_kwarg = 'product_pk'
    form_class = ProductForm
    context_object_name = 'product'
    permission_required = 'products.edit_prod'

    def get_success_url(self):
        return reverse('detailed_product', kwargs={'product_pk': self.object.pk})
    
class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    
    template_name = 'products/delete.html'
    pk_url_kwarg = 'product_pk'
    model = Products
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_prod'
    
class ModerateViews(PermissionRequiredMixin, ListView):
    permission_required = 'products.moderate_rev'
    template_name = 'accounts/moderate_page.html'
    context_object_name = 'reviews'
    model = Review
