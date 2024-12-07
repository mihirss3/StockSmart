from django.urls import path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),

    path('administrator/administer/user', AdminAdministerUserView.as_view(), name='adminAdministerUser'),
    path('administrator/administer/user/<str:emailId>', AdminAdministerUserView.as_view(), name='adminAdministerUser1'),

    path('administrator/administer/inventory', AdminAdministerInventoryView.as_view(), name='adminAdministerInventory'),
    path('administrator/administer/inventory/<str:inventory_id>', AdminAdministerInventoryView.as_view(), name='adminAdministerInventory1'),

    path('administrator/administer/supplier', AdminAdministerSupplierView.as_view(), name='adminAdministerSupplier'),
    path('administrator/administer/supplier/<int:supplier_id>', AdminAdministerSupplierView.as_view(), name='adminAdministerSupplier1'),

    path('administrator/administer/category', AdminAdministerCategoryView.as_view(), name='adminAdministerCategory'),
    path('administrator/administer/category/<int:category_id>', AdminAdministerCategoryView.as_view(), name='adminAdministerCategory1'),

    path('administrator/administer/product', AdminAdministerProductView.as_view(), name='adminAdministerProduct'),
    path('administrator/administer/product/<int:product_id>', AdminAdministerProductView.as_view(), name='adminAdministerProduct1'),

    path('administrator/administer/promotionaloffer', AdminAdministerPromotionalOfferView.as_view(), name='adminAdministerPromotionalOffer'),
    path('administrator/administer/promotionaloffer/<int:promotional_offer_id>', AdminAdministerPromotionalOfferView.as_view(),
         name='adminAdministerPromotionalOffer1'),

]
