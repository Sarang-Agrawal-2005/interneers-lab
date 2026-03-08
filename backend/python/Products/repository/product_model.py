# from django.db import models

# class ProductModel(models.Model):  # Django ORM model
#     sku = models.IntegerField(unique=True)
#     name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     reorder_level = models.IntegerField()

#     class Meta:
#         db_table = "products"

from mongoengine import Document, StringField, IntField, DateTimeField, ReferenceField, NULLIFY

from Products.repository.product_category_model import ProductCategoryModel

class ProductModel(Document):

    sku = IntField(required=True, unique=True)
    name = StringField(required=True)
    quantity = IntField(required=True)
    reorder_level = IntField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    category = ReferenceField(ProductCategoryModel, required = False, reverse_delete_rule=NULLIFY)

    meta = {
        "collection": "products"
    }