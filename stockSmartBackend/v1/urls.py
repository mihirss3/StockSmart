from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('hello', HelloView.as_view(), name='hello'),
    path('world', WorldView.as_view(), name='world'),
]
