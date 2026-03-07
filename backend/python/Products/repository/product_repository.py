from Products.domain.product import ProductEntity
from Products.repository.product_model import ProductModel

# called by the service layer to perform the actual crud operations
# handles actual crud operations and conversion logic between django/mongodb models and domain entties

class ProductRepository():

    def get_all(self):
        orm_products = ProductModel.objects()
        return [self.convert(p) for p in orm_products]
    
    def get_by_sku(self, sku):
        orm_product = ProductModel.objects(sku = sku).first()

        if not orm_product:
            return None
        return self.convert(orm_product)
        

    
    def create_product(self, payload: ProductEntity):
        orm_product = ProductModel(
            sku = payload.sku,
            name = payload.name,
            quantity = payload.quantity,
            reorder_level = payload.reorder_level,
            created_at = payload.created_at,
            updated_at = payload.updated_at

        )

        orm_product.save()

        return self.convert(orm_product)
    
    def update_product(self, sku, update_payload: ProductEntity):
        
        orm_product = ProductModel.objects(sku = sku).first()

        if not orm_product:
            return None

        orm_product.name = update_payload.name
        orm_product.quantity = update_payload.quantity
        orm_product.reorder_level = update_payload.reorder_level
        orm_product.updated_at = update_payload.updated_at

        orm_product.save()

        return self.convert(orm_product)
        
    
    def delete_product(self, sku):
        
        orm_product = ProductModel.objects(sku = sku).first()

        if not orm_product:
            return False

        orm_product.delete()
        return True
        
        
    
    def convert(self, orm_obj): # INTERNAL CONVERTER (ORM -> DOMAIN)
        return ProductEntity(
            sku=orm_obj.sku,
            name=orm_obj.name,
            quantity=orm_obj.quantity,
            reorder_level=orm_obj.reorder_level,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at
        )



