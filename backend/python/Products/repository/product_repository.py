from Products.domain.product import ProductEntity
from Products.models import ProductModel

# called by the service layer to perform the actual crud operations
# handles actual crud operations and conversion logic between django/mongodb models and domain entties

class ProductRepsoitory():

    def get_all(self):
        orm_products = ProductModel.objects.all()
        return [self.convert(p) for p in orm_products]
    
    def get_by_sku(self, sku):
        try:
            orm_product = ProductModel.objects.get(sku = sku)
            return self.convert(orm_product)
        except ProductModel.DoesNotExist:
            return None

    
    def create_product(self, payload: ProductEntity):
        orm_product = ProductModel.objects.create(
            sku = payload.sku,
            name = payload.name,
            quantity = payload.quantity,
            reorder_level = payload.reorder_level,

        )

        return self.convert(orm_product)
    
    def update_product(self, sku, update_payload: ProductEntity):
        try:
            orm_product = ProductModel.objects.get(sku = sku)

            orm_product.name = update_payload.name
            orm_product.quantity = update_payload.quantity
            orm_product.reorder_level = update_payload.reorder_level

            orm_product.save()

            return self.convert(orm_product)
        
        except ProductModel.DoesNotExist:
            return None
    
    def delete_product(self, sku):
        try:
            orm_product = ProductModel.objects.get(sku = sku)

            orm_product.delete()
            return True
        
        except ProductModel.DoesNotExist:
            return False
        
    
    
    # INTERNAL CONVERTER (ORM -> DOMAIN)
    # later we can switch from django orm to mongodb
    def convert(self, orm_obj):
        return ProductEntity(
            sku=orm_obj.sku,
            name=orm_obj.name,
            quantity=orm_obj.quantity,
            reorder_level=orm_obj.reorder_level
        )



