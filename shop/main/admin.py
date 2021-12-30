from django.contrib import admin
from .forms import PostAdminForm
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['name', 'category', 'available', 'slug', 'price', 'created']
    list_filter = ['name', 'available', 'slug', 'created']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['available', 'price']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


