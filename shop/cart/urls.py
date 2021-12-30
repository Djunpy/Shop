from django.urls import path
from .views import cart_add, cart_detail, cart_remove

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail_url'),
    path('add/<int:product_id>/', cart_add, name='cart_add_url'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove_url'),
]
