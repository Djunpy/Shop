from django.urls import path
from .views import IndexPage, SinglePage, ByCategory

app_name = 'main'

urlpatterns = [
    path('', IndexPage.as_view(), name='index_url'),
    path('category/<str:slug>/', ByCategory.as_view(), name='bycategory_url'),
    path('<int:id>/<str:slug>/', SinglePage.as_view(), name='single_url'),
]