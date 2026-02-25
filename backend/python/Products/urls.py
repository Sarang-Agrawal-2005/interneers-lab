from django.urls import path, include
from Products.api.product_views import list_products, get_product, create_product, update_product, delete_product


urlpatterns = [
    path('products/', list_products),
    path('products/<str:sku>/', get_product),
    path('products/create', create_product),
    path('products/update/<str:sku>/', update_product),
    path('products/delete/<str:sku>/', delete_product),
]
