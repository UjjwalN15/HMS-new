# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('department/', DepartmentApiView.as_view({'get': 'list', 'post': 'create'}), name='department'),
    path('department/<int:pk>/', DepartmentApiView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='department_detail'),
    path('billing/', BillingApiView.as_view({'get': 'list', 'post': 'create'}), name='billing'),
    path('billing/<int:pk>/', BillingApiView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='billing_detail'),
    path('product/', ProductApiView.as_view({'get': 'list', 'post': 'create'}), name='product'),
    path('product/<int:pk>/', ProductApiView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product_detail'),
    path('product_category/', ProductCategoryApiView.as_view({'get': 'list', 'post': 'create'}), name='product_category'),
    path('product_category/<int:pk>/', ProductCategoryApiView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product_category_detail'),
    path('supplier/', SupplierApiView.as_view({'get': 'list', 'post': 'create'}), name='supplier'),
    path('supplier/<int:pk>/', SupplierApiView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='supplier_detail'),
    path('expenses/', ExpensesApiView.as_view({'get': 'list', 'post': 'create'}), name='expenses'),
    path('expenses/<int:pk>/', ExpensesApiView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='expenses_detail'),
    path('report/', ReportViewSet.as_view({'get': 'list', 'post': 'create'}), name='report'),
    path('report/<int:pk>/', ReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='report_detail'),
    path('purchase_products/', PurchaseProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='purchase_product'),
    path('purchase_products/<int:pk>/', PurchaseProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='purchase_product'),
    path('revenue/', RevenueViewSet.as_view({'get': 'list', 'post': 'create'}), name='revenue'),
    path('revenue/<int:pk>/', RevenueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='revenue_detail'),
    path('purchase/', PurchaseApiView.as_view(), name='purchase'),
    path('purchase/<int:pk>/', PurchaseDetailApiView.as_view(), name='purchase_detail')
]
