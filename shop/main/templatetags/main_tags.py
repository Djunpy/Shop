from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('include/category.html')
def show_category():
    categories = Category.objects.all()
    return {'categories': categories}