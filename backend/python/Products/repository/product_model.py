from django.db import models

class ProductModel(models.Model):  # Django ORM model
    sku = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField()

    class Meta:
        db_table = "products"