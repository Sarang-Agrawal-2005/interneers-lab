from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from Products.repository.product_repository import ProductRepsository
from Products.service.product_service import ProductServices
from Products.domain.product_request import CreateProductRequest, UpdateProductRequest

repo = ProductRepsository()
service = ProductServices(repo)

@api_view(["GET"])
def list_products(request):
    products = service.list_products()
    data = [p.to_dict() for p in products]
    return Response(data, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_product(request, sku):
    product = service.get_product(sku)
    
    if not product:
        return Response({"error" : "Product not found"}, status = status.HTTP_404_NOT_FOUND)
    
    return Response(product.to_dict(), status = status.HTTP_200_OK)

@api_view(["POST"])
def create_product(request):
    data = request.data

    try:
        req = CreateProductRequest(
            sku=data.get("sku"),
            name=data.get("name"),
            quantity=data.get("quantity"),
            reorder_level=data.get("reorder_level")
        )

        created = service.create_product(req)

        return Response(created.to_dict(), status = status.HTTP_201_CREATED)
    
    except ValueError as e:
        return Response({"error" : str(e)}, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT"])
def update_product(request, sku):
    data = request.data

    req = UpdateProductRequest(
            name=data.get("name"),
            quantity=data.get("quantity"),
            reorder_level=data.get("reorder_level")
        )

    updated = service.update_product(sku, req)

    if not updated:
        return Response({"error" : "product not found"}, status = status.HTTP_404_NOT_FOUND)

    return Response(updated.to_dict(), status = status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_product(request, sku):
    deleted = service.delete_product(sku)

    if not deleted:
        return Response({"error" : "product not found"}, status = status.HTTP_404_NOT_FOUND)
    
    return Response({"message" : "product deleted"}, status=status.HTTP_200_OK)

    
   
