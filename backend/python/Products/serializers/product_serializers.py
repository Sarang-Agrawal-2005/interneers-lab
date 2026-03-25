from rest_framework import serializers

class CreateProductSerializer(serializers.Serializer): # automatic input validation
    sku = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=0)
    reorder_level = serializers.IntegerField(required=True, min_value=0)
    category_id = serializers.CharField(required=False)
    brand = serializers.CharField(required=True, allow_null=False)

class UpdateProductSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    quantity = serializers.IntegerField(required=False, min_value=0)
    reorder_level = serializers.IntegerField(required=False, min_value=0)
    category_id = serializers.CharField(required=False)
    brand = serializers.CharField(required=False, allow_null=False)

class ProductFilterSerializer(serializers.Serializer):
    categories = serializers.ListField(
        child = serializers.CharField(),
        required = False
    )

    brand = serializers.CharField(required = False)

    min_qty = serializers.IntegerField(required = False)
    max_qty = serializers.IntegerField(required = False)

    sort_by = serializers.ChoiceField(
        choices=["name", "sku", "brand", "quantity", "reorder_level", "created_at"],
        required = False
    )
    order = serializers.ChoiceField(
        choices=["asc", "desc"],
        required = False
    )

    page = serializers.IntegerField(min_value = 1, default = 1, required = False)
    page_size = serializers.IntegerField(min_value = 1, required = False)