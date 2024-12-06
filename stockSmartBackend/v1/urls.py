from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),

    path('administrator/administer/user', AdminAdministerUserView.as_view(), name='adminAdministerUser'),
    path('administrator/administer/user/<str:emailId>', AdminAdministerUserView.as_view(), name='adminAdministerUserForDelete'),

]
