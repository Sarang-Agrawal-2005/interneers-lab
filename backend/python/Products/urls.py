from django.urls import path, include
from Products.api.product_views import list_products, get_product, create_product, update_product, delete_product, bulk_create_products
from Products.api.product_category_views import list_categories, get_category, create_category, update_category, delete_category, get_products_of_category, add_product_to_category, remove_product_from_category


urlpatterns = [
    path('products/', list_products),
    path('products/<str:sku>/', get_product),
    path('products/create', create_product),
    path('products/update/<str:sku>/', update_product),
    path('products/delete/<str:sku>/', delete_product),

    path('categories/', list_categories),
    path('categories/<str:category_id>', get_category),
    path('categories/create/', create_category),
    path('categories/update/<str:category_id>/', update_category),
    path('categories/delete/<str:category_id>/', delete_category),

    path('categories/<str:category_id>/products/', get_products_of_category),
    path('categories/<str:category_id>/product/add', add_product_to_category),
    path('categories/<str:category_id>/product/remove/<str:sku>/', remove_product_from_category),

    path('products/create/bulk', bulk_create_products)
]
