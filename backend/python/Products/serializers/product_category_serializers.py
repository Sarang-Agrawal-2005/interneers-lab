from rest_framework import serializers

class CreateProductCategorySerializer(serializers.Serializer): # automatic input validation
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

class UpdateProductCategorySerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

class AddProductCategorySerializer(serializers.Serializer): # automatic input validation
    sku = serializers.IntegerField(required=True)