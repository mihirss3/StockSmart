from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products', ProductView.as_view(), name='products'),
    path('productsCount', ProductCountView.as_view(), name='productsCount'),
    path('top15ProductsExpiringSoon', Top15ProductsExpiringSoonView.as_view(), name='productsCount'),
]
