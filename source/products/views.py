from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from products.models import Products, Review
from django.contrib import auth
from django.shortcuts import get_object_or_404
from products.forms import ProductForm, ReviewForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin, FormView
# Create your views here.

class ProductListView(ListView):
    template_name = 'products/products_list.html'
    context_object_name = 'products'
    model = Products

class ProductDetailedView(FormView, DetailView):
    template_name = 'products/product_detailed.html'
    model = Products
    form_class = ReviewForm
    context_object_name = 'product'
    pk_url_kwarg = 'product_pk'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(kwargs)
        if form.is_valid():
            print(request.user.id)
            form.save(commit=False)
            form.author = request.user.id
            form.product = get_object_or_404(Products, pk=self.kwargs.get('product_pk'))
            print('yes')
            form.save()
        return reverse_lazy('detailed_product', pk=self.kwargs.get('product_pk'))

class ProductCreateView(CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductForm
    def get_success_url(self):
        return reverse('product_list')
    
class ProductUpdateView(UpdateView):
    model = Products
    template_name = 'products/product_update.html'
    pk_url_kwarg = 'product_pk'
    form_class = ProductForm
    context_object_name = 'product'
    #permission_required = 'main_app.change_projects'

    def get_success_url(self):
        return reverse('detailed_product', kwargs={'product_pk': self.object.pk})
    
class ProductDeleteView(DeleteView):
    template_name = 'products/product_delete.html'
    pk_url_kwarg = 'product_pk'
    model = Products
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')
    #permission_required = 'main_app.delete_projects'

class ReviewView(View):
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            product = Products.objects.filter(pk=self.kwargs.get('pk'))
            comment = form.save(commit=False)
            comment.author = request.user
            comment.product = product
            comment.save()
            print(request)
            return HttpResponse(status=200) 
        return reverse('detailed_product', kwargs={'product_pk': product.id})