from django.shortcuts import render
from .models import Product, Category
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from cart.forms import CartAddProductForm


class IndexPage(ListView):
    model = Product
    template_name = 'main/index.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True)


class SinglePage(FormMixin, DetailView):
    form_class = CartAddProductForm
    model = Product
    context_object_name = 'product'
    template_name = 'main/single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddProductForm
        return context


class ByCategory(ListView):
    template_name = 'main/by_category.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'], available=True)