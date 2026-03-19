from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone
from bson import ObjectId

from Products.repository.product_category_repository import ProductCategoryRepository
from Products.service.product_category_service import ProductCategoryServices
from Products.repository.product_repository import ProductRepository
from Products.service.product_service import ProductServices
from Products.domain.product_category_request import CreateProductCategoryRequest, UpdateProductCategoryRequest
from Products.serializers.product_category_serializers import CreateProductCategorySerializer, UpdateProductCategorySerializer

repo = ProductCategoryRepository()
service = ProductCategoryServices(repo)

product_repo = ProductRepository()
product_service = ProductServices(product_repo)

@api_view(["GET"])
def list_categories(request):
    categories = service.list_product_categories()
    data = [c.to_dict() for c in categories]

    return Response(data, status= status.HTTP_200_OK)

@api_view(["GET"])
def get_category(request, category_id):

    if not ObjectId.is_valid(category_id):
        return Response({"error" : "Invalid category id"}, status = status.HTTP_400_BAD_REQUEST)
    
    category = service.get_product_category(category_id)

    if not category:
        return Response({"error" : "Category does not exist"}, status = status.HTTP_404_NOT_FOUND)
    
    data = category.to_dict()

    return Response(data, status= status.HTTP_200_OK)

@api_view(["POST"])
def create_category(request):
    serializer = CreateProductCategorySerializer(data = request.data)

    if not serializer.is_valid():
        return Response({"error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        data = serializer.validated_data

        now = datetime.now(timezone.utc)

        req = CreateProductCategoryRequest(
            title = data.get("title"),
            description = data.get("description"),
            created_at = now,
            updated_at = now
        )

        created = service.create_product_category(req)

        return Response(created.to_dict(), status= status.HTTP_201_CREATED)
    
    except ValueError as e:
        return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["PUT"])
def update_category(request, category_id):

    if not ObjectId.is_valid(category_id):
        return Response({"error" : "Invalid category id"}, status = status.HTTP_400_BAD_REQUEST)
    
    serializer = UpdateProductCategorySerializer(data = request.data)

    if not serializer.is_valid():
        return Response({"error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        data = serializer.validated_data 

        req = UpdateProductCategoryRequest(
            title = data.get("title"),
            description = data.get("description"),
            updated_at = datetime.now(timezone.utc)
        )

        updated = service.update_product_category(category_id, req)

        if not updated:
            return Response({"error" : "Category does not exist"}, status = status.HTTP_404_NOT_FOUND)

        return Response(updated.to_dict(), status= status.HTTP_200_OK)
    
    except ValueError as e:
        return Response({"error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_category(request, category_id):

    if not ObjectId.is_valid(category_id):
        return Response({"error" : "Invalid category id"}, status = status.HTTP_400_BAD_REQUEST)

    deleted = service.delete_product_category(category_id)

    if not deleted:
        return Response({"error" : "Category does not exist"}, status = status.HTTP_404_NOT_FOUND)
    
    return Response({"message" : "Category deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_products_of_category(request, category_id):

    if not ObjectId.is_valid(category_id):
        return Response({"error" : "Invalid category id"}, status = status.HTTP_400_BAD_REQUEST)
    
    products = product_service.list_products_of_category(category_id)

    if products is None:
        return Response({"error" : "Category not found"}, status = status.HTTP_404_NOT_FOUND)
    
    data = [p.to_dict() for p in products]
    
    return Response(data, status = status.HTTP_200_OK)

@api_view(["PATCH"])
def add_product_to_category(request, category_id):

    if not ObjectId.is_valid(category_id):
        return Response({"error" : "Invalid category id"}, status = status.HTTP_400_BAD_REQUEST)
    
    data = request.data
    sku = data.get("sku")

    try:
        sku = int(sku)
    except ValueError as e:
        return Response({"error" : "sku must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        
        product = product_service.assign_category(sku, category_id)

        if product is None:
            return Response({"error": "Product not found"}, status= status.HTTP_404_NOT_FOUND)

        return Response(product.to_dict(), status= status.HTTP_200_OK)
    
    except ValueError as e:
        return Response({"error" : str(e)}, status = status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
def remove_product_from_category(request, category_id, sku):
    
    if not ObjectId.is_valid(category_id):
        return Response({"error" : "Invalid category id"}, status = status.HTTP_400_BAD_REQUEST)
    
    try:
        product = product_service.remove_category(sku, category_id)

        if product is None:
            return Response({"error": "Product not found"}, status= status.HTTP_404_NOT_FOUND)
        
        return Response(product.to_dict(), status= status.HTTP_200_OK)
    
    except ValueError as e:
        return Response({"error" : str(e)}, status = status.HTTP_400_BAD_REQUEST)